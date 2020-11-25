####################################
# Author: Joy                   
# File name: PriceComparator.py               
# Date created : 20/11/2020                   
# Python Version: 3.6               
####################################

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from tkinter import *
import os
import time
import logging as logger
import pyperclip


class Browser:
    def __init__(self,driverPath=None):
        self.driverPath = driverPath  

    #Initiate chromium driver
    def loadDriver(self):
        try:
            if self.driverPath is None:
                logger.error(" Please provide a driver path")
                return
            # open chrome options pass --incognito and --headless add_argument 
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--incognito")
            chrome_options.add_argument("--headless")
            self.driver = webdriver.Chrome(executable_path = self.driverPath , options=chrome_options)
            self.amazon()
        except Exception as e:
            logger.error(str(e))

    #Search Amazon for Product Price
    def amazon(self):
        myLabel = Label(root, text='Retrieving price from amazon..')
        myLabel.pack()
        root.update()
        try:
            if self.driver is None:
                logger.error(" Please provide an url")
                return
            self.driver.get('https://www.amazon.in')
            search = self.driver.find_element_by_name("field-keywords")
            search_btn = self.driver.find_element_by_xpath('//*[@class="nav-search-submit nav-sprite"]')
            search.send_keys(product)
            search_btn.click()

            #Get the Amazon first result URL
            first_result = self.driver.find_element_by_xpath('//*[@class="a-link-normal a-text-normal"][1]')
            global amazon_link
            amazon_link = first_result.get_attribute('href')
            self.driver.get(amazon_link)
            
            #Get Product Price
            global price_amazon
            price_amazon = self.driver.find_element_by_id('priceblock_ourprice').text
        
        except Exception as e:
            logger.error( str(e))

        self.flipkart()

    #Search Flipkart for Product Price
    def flipkart(self):
        myLabel = Label(root, text='Retrieving price from flipkart..')
        myLabel.pack()
        root.update()
        try:
            if self.driver is None:
                logger.error(" Please provide an url")
                return
            self.driver.get('https://flipkart.com')
            self.driver.find_element_by_xpath('//*[@class="_2KpZ6l _2doB4z"]').click()
            self.driver.find_element_by_name("q").send_keys(product)
            self.driver.find_element_by_xpath('//*[@class="L0Z3Pu"]').click()
            time.sleep(1)

            #Get Flipkart first result URL
            flipkart_result = self.driver.find_element_by_xpath('//*[@class="_1fQZEK"][1]')
            global flipkart_link
            flipkart_link = flipkart_result.get_attribute('href')
            self.driver.get(flipkart_link)

            #Get product price for Flipkart
            global price_flipkart
            price_flipkart = self.driver.find_element_by_xpath('//*[@class="_30jeq3 _16Jk6d"]').text
            
        except Exception as e:
            logger.error( str(e))

        print("Closing Chorome Driver..")
        self.driver.close()
        self.results()

    def results(self):
        myLabel = Label(root, text='Amazon: ' + price_amazon)
        myLabel.pack()
        myLabel = Label(root, text='Flipkart: ' + price_flipkart)
        myLabel.pack()
        flipkart_p = price_flipkart.strip()
        amazon_p = price_amazon.strip()
        flipkart_p = flipkart_p.replace(" ", "")
        amazon_p = amazon_p.replace(" ", "")
        flipkart_p = flipkart_p.replace(",", "")
        amazon_p = amazon_p.replace(",", "")
        flipkart_p = flipkart_p.replace("₹", "")
        amazon_p = amazon_p.replace("₹", "")
        flipkart_p = float(flipkart_p)
        amazon_p = float(amazon_p)
        if flipkart_p<amazon_p:
            myLabel = Label(root, text='Flipkart has the best deal!')
            myLabel.pack()
        if amazon_p<flipkart_p:
            myLabel = Label(root, text='Amazon has the best deal!')
            myLabel.pack()
        if amazon_p == flipkart_p:
            myLabel = Label(root, text='Both have the same deal!')
            myLabel.pack()
        amazonButton['state'] = NORMAL
        flipkartButton['state'] = NORMAL
        searchButton['state'] = NORMAL


def copyAmazon():
    pyperclip.copy(amazon_link)
def copyFlipkart():
    pyperclip.copy(flipkart_link)



def start():
    global product
    product = e.get()
    searchButton['state'] = DISABLED
    root.update()
    workinDir = os.path.dirname(os.path.realpath(__file__))  # current working Folder/Directory
    driverPath = workinDir.strip() + r"\Chromedriver\chromedriver.exe"
    
    browser = Browser(
        driverPath = driverPath,
        )
    browser.loadDriver()

root = Tk()
root.title("Price Comparator")

e = Entry(root, width=35, borderwidth=5)
e.pack()
product = "none"

searchButton = Button(root, text="Search for Product", command = start)
searchButton.pack()
amazonButton = Button(root, text="Copy Amazon Link", command = copyAmazon)
amazonButton.pack()
amazonButton['state'] = DISABLED
flipkartButton = Button(root, text="Copy Flipkart Link", command = copyFlipkart)
flipkartButton.pack()
flipkartButton['state'] = DISABLED
root.mainloop()