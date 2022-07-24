import configparser
from operator import contains
from matplotlib.pyplot import table
from numpy import identity
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import tkinter
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains


class EmailRequesAuto:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.email = self.config.get("login", 'email')
        self.password = self.config.get("login", "password")
        self.url = self.config.get("login", "url")

    def start_driver(self):
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()))
        self.driver.get(self.url)

    def tearDown(self):
        self.driver.quit()

    def login(self):
        self.start_driver()
        time.sleep(2)
        passInput = self.driver.find_element(By.CSS_SELECTOR, "input#pass")
        emailInput = self.driver.find_element(By.CSS_SELECTOR, "input#user")
        loginButton = self.driver.find_element(
            By.CSS_SELECTOR, "button#login_submit")
        emailInput.send_keys(self.email)
        passInput.send_keys(self.password)
        time.sleep(2)
        loginButton.click()
        print("login")

    def checkForNewEmail(self):
        self.login()
        time.sleep(8)
        table = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.ID, 'messagelist')))
        tablebody = table.find_element(By.TAG_NAME, "tbody")
        listOFUnreadMsg = tablebody.find_elements(
            By.CSS_SELECTOR, 'tr.message')
        a = listOFUnreadMsg[0].find_element(By.CSS_SELECTOR,
                                            "span.subject a")
        a.click()
        time.sleep(7)
        self.driver.get(a.get_attribute("href"))
        data = []
        x = 0
        while x < 6:
            email_body = self.driver.find_element(By.CLASS_NAME, "rcmBody")
            if "Hello there!" in self.driver.find_element(By.CSS_SELECTOR, "h2.subject").text:
                infos = email_body.find_elements(By.TAG_NAME, "p")
                data.append({"user_id": infos[0].text.split(":")[1],
                            "first_name": infos[1].text.split(":")[1], "last_name": infos[2].text.split(":")[1], "city": infos[3].text.split(":")[1],
                             "postal_code": infos[4].text.split(":")[1], "country": infos[5].text.split(":")[1], "home_address": infos[6].text.split(":")[1],
                             "email": infos[7].text.split(":")[1], "identity_type": infos[8].text.split(":")[1]})

            self.driver.find_element(By.ID, "rcmbtn120").click()
            x = x + 1
        print("-----------------")
        df = pd.DataFrame(data)
        df.to_csv("./jaiza_csv.csv", sep=";")
        print(df)
        print("-----------------")


if __name__ == '__main__':
    em = EmailRequesAuto()
    em.checkForNewEmail()
    em.tearDown()
