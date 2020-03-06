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

dict = {"a": 1, "b": 2, "c": 4}

with open("test.txt", "w+") as fp:
    json.dump(dict, fp)
