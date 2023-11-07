"""Script Summary
Reads lines from the stdin:
  CAT table.csv | PYTHON save_html.py
Logs into the fake linkedin account,
then takes each url and saves html of the linkedin page
"""

import logging
import time
import os

from random import randint

from bs4 import BeautifulSoup
from selenium import webdriver

from linkedin_parser.config import config


logger = logging.getLogger('linkedin_parser')


# get filename to save with
def get_file_name(line):
    splitted = line.split(",")
    
    linkedin_url = splitted[1].strip()
    logger.debug(linkedin_url)
    name_list = splitted[0].strip().split(" ")
    name_list.append(linkedin_url.split('/')[4])
    return '_'.join(name_list) + '.html'


# input: current line
# output: html code as a soup object
def get_soup(driver, line):
    linkedin_url = line.split(",")[1].strip()
    url_extention = "?trk=public-profile-join-page"
    linkedin_url += url_extention
    driver.get(linkedin_url)
    return BeautifulSoup(driver.page_source, "lxml")


def save_html(lines, save_dir):
    logger.info(f"Saving HTML files to {save_dir}...")
    '''
    #virtual display setup when working from a server
    display = Display(visible=0, size=(800, 600))
    display.start()
    '''

    # chrome setup
    
    chrome_options = webdriver.ChromeOptions()
    for opt in config.BROWSER['chrome_options']:
       chrome_options.add_argument(opt)
    # chrome_options.add_argument(f'--proxy-server={config.BROWSER['proxy']}')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    
    driver = webdriver.Chrome()
    # linkedin setup
    login_url = 'https://www.linkedin.com/uas/login'
    driver.get(login_url)
    time.sleep(10)
    email = driver.find_element_by_id("session_key-login")
    password = driver.find_element_by_id("session_password-login")
    email.send_keys(config.LINKEDIN['email'])
    time.sleep(1)
    password.send_keys(config.LINKEDIN['password'])
    time.sleep(1)
    driver.find_element_by_name("signin").click()

    for line in lines:
        file_name = get_file_name(line)
        linkedin_soup = get_soup(driver, line)
        time.sleep(randint(5, 8))

        path = os.path.join(save_dir, file_name)
        with open(path, "w") as f:
            f.write(str(linkedin_soup))

        # json testing
        """
        json_object = json.dumps(file_name)
        print(json_object)
        
        ContentUrl = json.dumps({
          'url': str(urls),
          'uid': str(uniqueID),
          'page_content': file_name,
          'date': timestamp()
        })
        """

    driver.quit()
