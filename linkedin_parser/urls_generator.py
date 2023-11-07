"""Script Summary
Reads lines from GitHubProfiles table in the database, finds people's
linkedin urls from top 5 duckduckgo results, and creates a csv file with
columns:[Name   Url]
"""

from bs4 import BeautifulSoup

from difflib import SequenceMatcher
from random import randint
import urllib.parse
import logging
import sys
import time
import requests
import csv

# import psycopg2

logger = logging.getLogger('linkedin_parser')


# checks similarity betweeb two string objects
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


# input example: [1739 git://github.com/pallets/werkzeug.git Python  Armin Ronacher  ]
# output: Armin Ronacher,https://www.linkedin.com/in/arminronacher
def get_name_and_url(line):
    fields = line.strip().split(",")
    real_name = fields[2] + " " + fields[3]
    skills = fields[4]
    logger.debug(real_name)
    if not real_name.replace(" ", "").isalpha():
        return
    # query example: 'David Brown JavaScript linkedin'
    query = real_name + " skills "+ skills+" linkedin"
    # query = real_name+" "+skill+" linkedin"
    duck_url = 'https://duckduckgo.com/html/?q=%s' % query
    html_duck_url = requests.get(duck_url).text

    duck_soup = BeautifulSoup(html_duck_url, "lxml")
    duck_results = duck_soup.findAll("a", class_="result__a")[:4]
    output = None
    logger.debug("real: " + real_name)
    for result in duck_results:
        linkedin_url = "https://" + str(result['href'].strip()[29:])
        linkedin_url = urllib.parse.unquote(linkedin_url)
        output = None
        # logger.debug(linkedin_url[:28])
        if linkedin_url.startswith('https://www.linkedin.com/in/'):
            duck_name_list = []
            for name in result.findAll("b"):
                duck_name_list.append(name.get_text())
            duck_name = " ".join(duck_name_list)
            # [:-1]
            logger.debug("duck " + duck_name)
            if similar(real_name, duck_name) >= 0.5:
                output = linkedin_url
                break

    if output is None:
        return

    new_row = {'Name': real_name, 'Url': output};
    logger.debug(new_row)
    logger.debug("\n")
    return new_row


def generate_search_urls(lines, save_file):
    logger.info(f"Saving URLs into {save_file}...")
    # file save setup
    FIELD_NAMES = ['Name', 'Url']

    # database connection
    """
    db = psycopg2.connect(host="localhost",database="talent", user="talent", password="lopedevega")
    c = db.cursor()
    c.execute("SELECT github_id, github_name FROM github_profiles")
    rows = c.fetchall()
    db.close();
    """

    with open(save_file, "w") as f:
        writer = csv.DictWriter(f, fieldnames=FIELD_NAMES, dialect='excel')
        row_count = 0;
        success_rows = 0
        for line in lines:
            new_row = get_name_and_url(line)
            if new_row is not None:
                writer.writerow(new_row)
                success_rows += 1
            time.sleep(randint(4, 7))
            row_count += 1
        logger.debug(str(success_rows) + "/" + str(row_count))
