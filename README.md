# TravianClassementExporter

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/3456684829174978b0bab58a1442e227)](https://www.codacy.com/manual/Harkame/TravianClassementExporter?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Harkame/TravianClassementExporter&amp;utm_campaign=Badge_Grade)
[![Maintainability](https://api.codeclimate.com/v1/badges/d7fa2efd92e6c6ba49a0/maintainability)](https://codeclimate.com/github/Harkame/TravianClassementExporter/maintainability)

Script that export classement to json files

## Installation

``` bash

pip install -r requirements.txt

```

## Usage

``` bash

usage: main.py [-h] -i IDENTIFIANT -p PASSWORD

Script to download travian classements

optional arguments:
  -h, --help            show this help message and exit
  -i IDENTIFIANT, --identifiant IDENTIFIANT
                        Travian identifiant (username or email)
                        Required to get classements
                        Example : python tce/main.py -i myusername
  -p PASSWORD, --password PASSWORD
                        Travian password
                        Required to get classements
                        Example : python tce/main.py -p mypassword

```
