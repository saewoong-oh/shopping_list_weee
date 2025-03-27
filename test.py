from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time


driver = webdriver.Chrome()


TEST_URL="https://www.safeway.com"
url = driver.get(TEST_URL)
time.sleep(5000)

