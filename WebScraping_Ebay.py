#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 18:31:09 2024

@author: filippobalbo
"""

from bs4 import BeautifulSoup
import requests
import datetime
import time
import datetime
import pandas as pd
import re
import csv
import smtplib


def check_price():
    # Connect to the website:
    initial_url = "https://www.kleinanzeigen.de/s-berlin/sortierung:preis"
    end_url = "dr-martens-43/k0l3331"
    base_url = "https://www.kleinanzeigen.de/s-berlin/sortierung:preis/dr-martens-43/k0l3331"
    headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
    
    # Initialize lists
    clean_prices = [] 
    clean_titles = []   
    date = []
    
    # Send GET request for the base URL:
    base_page = requests.get(base_url, headers=headers)
    base_soup = BeautifulSoup(base_page.content, "html.parser")
    base_soup2 = BeautifulSoup(base_soup.prettify(), "html.parser")
    
    # Find the total number of pages
    total_pages = 3   
     
    # Create a list of numbers from 1 to 4
    numbers_list = [number for number in range(1, 5)]
    #print(numbers_list)
    
    # Loop through each page:
    for page_num in range (1,4):
        if page_num == 1:
            url = base_url
        else: url = f"{initial_url}/seite:{page_num}/{end_url}"
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")
        title2 = soup.find_all('a',class_ = 'ellipsis')
        price2 = soup.find_all('p',class_ = 'aditem-main--middle--price-shipping--price')
        for titles in title2:
            title = titles.get_text(strip=True)
            clean_titles.append(title)    
        for prices in price2: 
            price = prices.get_text(strip=True)
            clean_prices.append(price)       
    
    # Find today data:
    date = datetime.date.today()
    
    # Create DataFrame from the scraped data:
    df = pd.DataFrame({"Title": clean_titles, "Price": clean_prices, "Date":date})
    #print(df)
    
    # Save DataFrame to a CSV file:
    df.to_csv('kleinanzeigen_data.csv', index=False)


# Runs check_price after a set time and inputs data into your CSV
# while(True):
check_price()
#     time.sleep(86400)

# Reading the csv file:   
df = pd.read_csv("/Users/filippobalbo/Documents/Documents/Financial Projects/Web Scraping/kleinanzeigen_data.csv")    
print(df)

