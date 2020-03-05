import datetime
import logging
import os
import re
import sys
import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

logger = logging.getLogger("travianscraper")

TRAVIAN_URL = "https://www.travian.com/fr/gameworld/login"

player_list = []


class TravianScraper:
    session = None

    def __init__(self, session):
        self.session = session


def parse_classement_page(driver):

    hrefs = []

    for player in driver.find_elements_by_css_selector("tbody tr td.pla a"):
        hrefs.append(player.get_attribute("href"))

    for href in hrefs:
        driver.get(href)

        time.sleep(1)

        parse_player_page(driver)

    with open("players.json", "w") as fp:
        json.dump(player_list, fp)


def parse_player_page(driver):
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "tbody"))
    )

    fields = driver.find_elements_by_css_selector("tbody tr")

    player = {}

    player["pseudo"] = driver.find_element_by_css_selector(".titleInHeader").text
    player["faction"] = fields[1].find_element_by_css_selector("td").text
    player["alliance"] = fields[2].find_element_by_css_selector("td a").text
    player["population_classement"] = fields[4].find_element_by_css_selector("td").text
    player["population_score"] = fields[4].find_element_by_css_selector("td span").text
    player["off_classement"] = fields[5].find_element_by_css_selector("td").text
    player["off_score"] = fields[4].find_element_by_css_selector("td span").text
    player["def_classement"] = fields[6].find_element_by_css_selector("td").text
    player["def_score"] = fields[4].find_element_by_css_selector("td span").text
    player["hero_level"] = fields[7].find_element_by_css_selector("td").text
    player["hero_experience"] = fields[4].find_element_by_css_selector("td span").text

    player_list.append(player)

    return


if __name__ == "__main__":
    """
    scraper = TravianScraper(requests.session())

    if not scraper.login("https://www.travian.com/fr/gameworld/login", "id", "pass"):
        print("Login failed")
        sys.exit()

    details_page = scraper.extract_details(
        "https://ts3.travian.fr/spieler.php?uid=25357"
    )
    """

    driver = webdriver.Chrome("chromedriver.exe")
    driver.get("https://www.travian.com/fr#login")

    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".worldGroup .world:nth-child(3)"))
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
    input_username.send_keys("fe")

    input_password = driver.find_element_by_css_selector("input[name='password']")
    input_password.clear()
    input_password.send_keys("ef")

    button_login = driver.find_element_by_css_selector('button[type="submit"]')
    button_login.click()

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.statistics"))
    )

    driver.get("https://ts3.travian.fr/statistiken.php")

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.paginator"))
    )

    pages_number = driver.find_elements_by_css_selector("div.paginator a")

    first_page = 1
    last_page = int(pages_number[-1:][0].text)

    driver.get("https://ts3.travian.fr/statistiken.php?id=0&page=" + str(first_page))

    for page in range(first_page, last_page):
        driver.get("https://ts3.travian.fr/statistiken.php?id=0&page=" + str(page))

        parse_classement_page(driver)

# driver.close()

##scraper.

# scraper.logout()
