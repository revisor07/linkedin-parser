"""Script Summary
Scans the hardcoded directory, reads each html file and extracts
the necessary info, which is saved into a .csv file with the
first column being name, and others corrspond to other info
"""

import csv
import os
import logging

from bs4 import BeautifulSoup

logger = logging.getLogger('linkedin_parser')


def process_html(filepath):
    with open(filepath, "r") as f:
        soup = BeautifulSoup(f, "lxml")
        education = []
        experience = []
        skills = []

        name = soup.find("div", class_="pv-top-card-section__body").div.div.h1.get_text()
        place = soup.find("div", class_="pv-top-card-section__information mt3 ember-view").find("h3",
                                                                                                class_="pv-top-card-section__location Sans-17px-black-70% mb1 inline-block").get_text().strip()
        exp_list = soup.findAll("li",
                                class_="pv-profile-section__card-item pv-position-entity ember-view")
        edu_list = soup.findAll("li", class_="pv-education-entity pv-profile-section__card-item ember-view")
        skill_list = soup.findAll("li",
                                  class_="pv-skill-entity--featured pb5 pv-skill-entity relative pv-skill-entity--include-highlights ember-view")
        for exp in exp_list:
            company = exp.find("span",
                               class_="pv-entity__secondary-title").get_text().strip()
            date_range = exp.find("h4",
                                  class_="pv-entity__date-range inline-block Sans-15px-black-70%").findAll("span")[
                1].get_text().strip()
            experience.append(company + "(" + date_range + ")")
            logger.debug(company)
            logger.debug(date_range)
        for edu in edu_list:
            school = edu.find("div", "pv-entity__degree-info").h3.get_text()
            date_range_list = edu.find("p", class_="pv-entity__dates Sans-15px-black-70%").findAll("span")[1].findAll(
                "time")
            date_range = date_range_list[0].get_text() + "-" + date_range_list[1].get_text()
            education.append(school + "(" + date_range + ")")
            logger.debug(school)
            logger.debug(date_range)
        for raw_skill in skill_list:
            skill = raw_skill.div.div.a.div.findAll("span")[0].get_text()
            skills.append(skill)
            logger.debug(skill)
            logger.debug(name)
        logger.debug(place)
        return {'Name': name, 'Place': place, 'Experience': experience, 'Education': education}


def extract_info(html_path, save_file):
    logger.info(f"Extracting info from {html_path}...")
    FIELD_NAMES = ['Name', 'Place', 'Experience', 'Education']
    with open(save_file, "w") as f:
        writer = csv.DictWriter(f, fieldnames=FIELD_NAMES, dialect='excel')
        writer.writeheader()
        for file in os.listdir(html_path):
            if file.endswith(".html"):
                new_row = process_html(os.path.join(html_path, file))
                logger.debug("\n")
                try:
                    writer.writerow(new_row)
                except UnicodeEncodeError:
                    logger.debug("UnicodeEncodeError")
