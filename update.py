from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select

from getpass import getpass

import pymysql
from db import app

class Database:
    def __init__(self):
        host = app.config.get('DB_IP')
        user = app.config.get('DB_USER')
        #password = app.config.get('DB_PASS')
        db = 'fpl'
        sock = '/var/run/mysqld/mysqld.sock'
        self.con = pymysql.connect(host=host, user=user, \
                                   db=db, unix_socket=sock, cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()

db = Database()

options = webdriver.FirefoxOptions()
options.add_argument('-headless')
driver = webdriver.Firefox(firefox_options=options)

# go to FPL website
driver.get('https://fantasy.premierleague.com/transfers')

# log in
delay = 3 # seconds
try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, \
             'loginUsername')))
except TimeoutException:
    print("Loading took > 3 secs. Check the page is loading properly.")
email = driver.find_element_by_id("loginUsername")
username = input("Enter FPL username: ")
email.send_keys(username)
password = driver.find_element_by_id("loginPassword")
pswd = getpass('Password: ')
password.send_keys(pswd)
submit_div = driver.find_element_by_class_name("Login__LoginButtonWrap-sc-1dpiyoc-3.jEGIBP")
submit = submit_div.find_element_by_class_name("ArrowButton-thcy3w-0.hHgZrv")
submit.click()
driver.get('https://fantasy.premierleague.com/transfers')

# filter by position
try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, \
             'filter')))
except TimeoutException:
    print("Loading took > 3 secs. Check the page is loading properly.")
select = Select(driver.find_element_by_id('filter'))

positions = ['Forwards', 'Defenders', 'Midfielders', 'Goalkeepers']
for p in positions:
    select.select_by_visible_text(p)
    # set number of pages to check depending on position
    if p == 'Forwards' or p == 'Goalkeepers':
        pages = 1
    else:
        pages = 3
    for page in range(0, pages):
        rows = driver.find_elements_by_class_name("ElementTable__ElementRow-sc-1v08od9-3.ElementListRow__StyledElementListRow-sc-122fdeq-0.bXpRqg")
        for row in rows:
            name_td = row.find_element_by_class_name("ElementTable__ElementCell-sc-1v08od9-4.iQqEvn")
            name = name_td.find_element_by_class_name("ElementInTable__Name-y9xi40-1.eyyBOW")
            pname = name.get_attribute('innerHTML')
            team = name_td.find_element_by_class_name("ElementInTable__Team-y9xi40-2.hCvdTQ")
            pteam = team.get_attribute('innerHTML')
            stats_tds = row.find_elements_by_class_name("ElementListRow__ElementListStatCell-sc-122fdeq-1.hznghq")
            price = stats_tds[0].get_attribute('innerHTML')
            points = stats_tds[1].get_attribute('innerHTML')
            # calculate value (PPM)
            if p == 'Defenders' or p == 'Goalkeepers':
                base_price = 4.0
            else:
                base_price = 4.5
            true_price = float(price) - base_price
            if abs(true_price - 0) > 1e-3:
                value = float(points)/true_price
            else:
                value = float(points)/0.5
            # calculate deviation using regression data
            deviation = float(points) - 18.53*float(price) - 0.22
            if p == 'Goalkeepers':
                deviation_by_pos = float(points) - 81.04*float(price) + 314.41
            if p == 'Defenders':
                deviation_by_pos = float(points) - 40.76*float(price) + 122.38
            if p == 'Midfielders':
                deviation_by_pos = float(points) - 19.73*float(price) + 22.63
            if p == 'Forwards':
                deviation_by_pos = float(points) - 22.87*float(price) + 47.77
            db.cur.execute("INSERT IGNORE INTO players (name, club, position, price, points, value,\
                           deviation, deviation_by_pos) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", \
                          (pname, pteam, p[:-1], price, points, value, deviation, deviation_by_pos))
            db.con.commit()
        right_arrow = driver.find_element_by_class_name("Chevrons__ChevronRight-ifqxdy-1.kjNwMl")
        page_forward = right_arrow.find_element_by_xpath('..')
        page_forward.click()
