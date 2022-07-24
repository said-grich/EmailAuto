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
        self.unread_msgs = []

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

    def collectUnreadUrls(self):
        self.login()
        time.sleep(8)
        table = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.ID, 'messagelist')))
        tablebody = table.find_element(By.TAG_NAME, "tbody")
        listOFUnreadMsg = tablebody.find_elements(
            By.CSS_SELECTOR, 'tr.message')
        for msg in listOFUnreadMsg:
            if "Hello there!" in msg.find_element(By.CSS_SELECTOR,
                                                  "span.subject a span").text:
                a = msg.find_element(By.CSS_SELECTOR,
                                     "span.subject a")
                a.click()
                time.sleep(3)
                self.unread_msgs.append(a.get_attribute("href"))

    def checkForNewEmail(self):
        data = []
        self.collectUnreadUrls()
        for msg in self.unread_msgs:
            self.driver.get(msg)
            email_body = self.driver.find_element(By.CLASS_NAME, "rcmBody")
            infos = email_body.find_elements(By.TAG_NAME, "p")
            data.append({"user_id": infos[0].text.split(":")[1],
                         "first_name": infos[1].text.split(":")[1], "last_name": infos[2].text.split(":")[1], "city": infos[3].text.split(":")[1],
                         "postal_code": infos[4].text.split(":")[1], "country": infos[5].text.split(":")[1], "home_address": infos[6].text.split(":")[1],
                         "email": infos[7].text.split(":")[1], "identity_type": infos[8].text.split(":")[1]})
        df = pd.DataFrame(data)
        print("-----------------")
        print(df)
        print("-----------------")
        df.to_csv("./jaiza_csv.csv", sep=";")

    def mergeTempMails(self):
        self.config.read('config.ini')
        jaiza_csv_path = self.config.get("csv", 'jaiza')
        temp_csv_path = self.config.get("csv", 'tempmail')
        temp_csv = pd.read_csv(temp_csv_path, sep=",")
        jaiza_csv = pd.read_csv(jaiza_csv_path, sep=";")

        jaiza_csv["login_mails"] = temp_csv.mail.str.cat(temp_csv.provider)
        jaiza_csv["phone_number"] = temp_csv["phone number"]
        jaiza_csv["password"] = temp_csv["pswd"]
        jaiza_csv.to_csv("./csv_final.csv", sep=";")


if __name__ == '__main__':
    em = EmailRequesAuto()
    em.checkForNewEmail()
    em.tearDown()
    # em.mergeTempMails()
