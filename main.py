import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import tkinter
from tkinter import Tk, Canvas, Entry,Button, PhotoImage
from pathlib import Path
from selenium.webdriver.support import expected_conditions as EC


from selenium.webdriver.support.wait import WebDriverWait


class EmailRequesAuto:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.email = self.config.get("login", 'email')
        self.password = self.config.get("login", "password")
        self.url=""

    def start_driver(self):
        self.driver = webdriver.Firefox()
        self.driver.get(self.url)
    def login(self):
        self.url="https://webmail.jaiza.io/";
        self.start_driver();
        time.sleep(2);
        passInput=self.driver.find_element(By.CSS_SELECTOR,"input#pass");
        emailInput=self.driver.find_element(By.CSS_SELECTOR,"input#user");
        loginButton=self.driver.find_element(By.CSS_SELECTOR,"button#login_submit");
        emailInput.send_keys(self.email);
        passInput.send_keys(self.password);
        time.sleep(2);
        loginButton.click();
        print("login");
    def checkForNewEmail(self):
        self.login();
        time.sleep(20)
        table=WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'messagelist')))
        tablebody=table.find_element(By.TAG_NAME,"tbody");
        listOFUnreadMsg=tablebody.find_elements(By.CSS_SELECTOR,'tr.message.unread');
        print(len(listOFUnreadMsg));
        for element in listOFUnreadMsg:
            if(element.find_element(By.XPATH,"td.subject span.subject a span").tex):
            a=element.find_element(By.TAG_NAME,"a");
            a.click();


if __name__ == '__main__':
    em=EmailRequesAuto();
    em.checkForNewEmail();

