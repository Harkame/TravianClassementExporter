import logging
import re
import json
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from tqdm import tqdm

if __package__ is None or __package__ == "":
    from helpers import (
        get_arguments,
        get_config,
        strip_accents,
    )
else:
    from .helpers import (
        get_arguments,
        get_config,
        strip_accents,
    )

logger = logging.getLogger("tce")

TRAVIAN_URL = "https://www.travian.com/fr/gameworld/login"

player_list = []


class TravianClassementExporter:
    session = None

    def __init__(self):
        self.identifiant = ""
        self.password = ""
        self.driver_path = ""
        self.bar = None

    def init_arguments(self):
        arguments = get_arguments(None)

        if arguments.verbose:
            logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                "%(asctime)s :: %(levelname)s :: %(module)s :: %(lineno)s :: %(funcName)s :: %(message)s"
            )
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)

            if arguments.verbose == 0:
                logger.setLevel(logging.NOTSET)
            elif arguments.verbose == 1:
                logger.setLevel(logging.DEBUG)
            elif arguments.verbose == 2:
                logger.setLevel(logging.INFO)
            elif arguments.verbose == 3:
                logger.setLevel(logging.WARNING)
            elif arguments.verbose == 4:
                logger.setLevel(logging.ERROR)
            elif arguments.verbose == 5:
                logger.setLevel(logging.CRITICAL)

            logger.addHandler(stream_handler)

        if arguments.identifiant is not None:
            self.identifiant = arguments.identifiant

        if arguments.password is not None:
            self.password = arguments.password

        if arguments.driver is not None:
            self.driver_path = arguments.driver

        logger.debug("identifiant : %s", self.identifiant)
        logger.debug("password : %s", self.password)

    def init_config(self):
        config = get_config(self.config_file)

        # TODO

    def parse_classement_page(self, driver):

        hrefs = []

        for player in driver.find_elements_by_css_selector("tbody tr td.pla a"):
            hrefs.append(player.get_attribute("href"))

        for href in hrefs:
            driver.get(href)

            self.parse_player_page(driver)

            self.bar.update(1)

    def parse_player_page(self, driver):
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "tbody"))
        )

        fields = driver.find_elements_by_css_selector("tbody tr")

        player = {}

        player["pseudo"] = driver.find_element_by_css_selector(".titleInHeader").text
        player["faction"] = fields[1].find_element_by_css_selector("td").text

        try:
            player["alliance"] = fields[2].find_element_by_css_selector("td a").text
        except NoSuchElementException:
            player["alliance"] = ""

        player["population_classement"] = (
            fields[4].find_element_by_css_selector("td").text
        )
        player["population_score"] = (
            fields[4].find_element_by_css_selector("td span").text
        )
        player["off_classement"] = fields[5].find_element_by_css_selector("td").text
        player["off_score"] = fields[5].find_element_by_css_selector("td span").text
        player["def_classement"] = fields[6].find_element_by_css_selector("td").text
        player["def_score"] = fields[6].find_element_by_css_selector("td span").text
        player["hero_level"] = fields[7].find_element_by_css_selector("td").text
        player["hero_experience"] = (
            fields[4].find_element_by_css_selector("td span").text
        )

        player_list.append(player)

    def run(self):
        driver = webdriver.Chrome(self.driver_path)
        driver.get("https://www.travian.com/fr#login")

        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".worldGroup .world:nth-child(3)")
            )
        ).click()

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[name='usernameOrEmail']")
            )
        )

        input_username = driver.find_element_by_css_selector(
            "input[name='usernameOrEmail']"
        )
        input_username.clear()
        input_username.send_keys(self.identifiant)

        input_password = driver.find_element_by_css_selector("input[name='password']")
        input_password.clear()
        input_password.send_keys(self.password)

        button_login = driver.find_element_by_css_selector('button[type="submit"]')
        button_login.click()

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.statistics"))
        )

        driver.get("https://ts3.travian.fr/statistiken.php")

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.paginator"))
        )

        time.sleep(1)

        pages_number = driver.find_elements_by_css_selector("div.paginator a")

        first_page = 1
        last_page = int(pages_number[-3:][0].text)

        self.bar = tqdm(
            total=last_page * 20,  # 20players / page
            position=1,
            bar_format="[{bar}] - [{n_fmt}/{total_fmt}] - [players]",
        )

        for page in range(first_page, last_page * 20):
            driver.get("https://ts3.travian.fr/statistiken.php?id=0&page=" + str(page))

            self.parse_classement_page(driver)

            with open("players.json", "w") as fp:  # save after each page
                json.dump(player_list, fp)

        self.bar.close()
