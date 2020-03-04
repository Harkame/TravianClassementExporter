import datetime
import logging
import os
import re
import sys
import requests
from bs4 import BeautifulSoup
import json

logger = logging.getLogger("travianscraper")

TRAVIAN_URL = "https://www.travian.com/fr/gameworld/login"


class TravianScraper:
    session = None

    def __init__(self, session):
        self.session = session

    def login(self, url, identifiant, password):
        self.session.cookies.clear()

        headers = {
            "Content-Type": "application/json",
        }

        form_data = {}

        data = {
            "gameWorld": {"url": url},
            "usernameOrEmail": identifiant,
            "password": password,
        }

        print(json.dumps(data))

        response = self.session.post(TRAVIAN_URL, json=data, headers=headers)

        logger.debug("status_code : %s", response.status_code)

        yggtorrent_token = None

        print(response.json())
        print(response.status_code)

        if response.status_code == 200:
            logger.debug("Login successful")

            return True
        else:
            logger.debug("Login failed")

            return False

    def logout(self):
        """
        Logout request
        """
        response = self.session.get(YGGTORRENT_LOGOUT_URL)

        self.session.cookies.clear()

        logger.debug("status_code : %s", response.status_code)

        if response.status_code == 200:
            logger.debug("Logout successful")

            return True
        else:
            logger.debug("Logout failed")

            return False

    def extract_details(self, url):
        response = self.session.get(url)

        details_page = BeautifulSoup(response.content, features="lxml")

        return details_page


if __name__ == "__main__":
    scraper = TravianScraper(requests.session())

    if not scraper.login("https://www.travian.com/fr/gameworld/login", "id", "pass"):
        print("Login failed")
        sys.exit()

    details_page = scraper.extract_details(
        "https://ts3.travian.fr/spieler.php?uid=25357"
    )

    print(details_page)

    ##scraper.

    # scraper.logout()
