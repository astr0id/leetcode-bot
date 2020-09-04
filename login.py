from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from subprocess import Popen, PIPE

import json
import time
import re
import os
import sys

import config

cap = DesiredCapabilities().FIREFOX
cap["marionette"] = False
fp = webdriver.FirefoxProfile('/home/lin/.mozilla/firefox/1g16lozf.bot')
options = Options()
options.headless = True
driver = webdriver.Firefox(capabilities=cap, options=options, executable_path="./driver/geckodriver", firefox_profile=fp)
Account, Password = config.email, config.passwd

def login():
    login_url = "https://leetcode.com/accounts/login/"
    delay = 5 # seconds

    try:
        driver.get(login_url)
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, "home-app")))
        print('Already logged in')
        return True
    except TimeoutException:
        print("Start Login")
        if Account and Password:
            driver.get(login_url)

            username = driver.find_element_by_id("id_login")
            password = driver.find_element_by_id("id_password")
            
            username.send_keys(Account)
            password.send_keys(Password)

            driver.find_element_by_name("signin_btn").click()

            try:
                myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, "home-app")))
                #print "Page is ready!"
                return True
            except TimeoutException:
                print("Loading took too much time!")
                return False
            
if __name__ == "__main__":
    if login():
        p = Popen('leetcode user -l', shell=True, stdin=PIPE)
        s = Account+'\n'+Password+'\n'
        p.communicate(input=s.encode('utf8'))
        res = os.popen('leetcode list -q eD').readlines()
        if len(res) > 0:
            print('Login Successfully!')
            # print(res)
        else:
            print('Login Failed')
            print(res)