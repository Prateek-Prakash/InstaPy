import configparser
import starlette.responses
import time

from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Driver Setup
executable_path = "./chromedriver"
options = webdriver.ChromeOptions()
options.add_argument("--no-proxy-server")
options.add_argument("--disable-extensions")
options.add_argument('--hide-scrollbars')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(executable_path=executable_path, options=options)
driver.get("https://www.instagram.com")

# Config
config = configparser.ConfigParser()
config.read("config.ini")

# Login
time.sleep(5)
username = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
password = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
username.clear()
password.clear()
username.send_keys(config.get("INSTAGRAM", "USERNAME"))
password.send_keys(config.get("INSTAGRAM", "PASSWORD"))
login = driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

# Skip Save Login
time.sleep(10)
not_now = driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]").click()

# Skip Notifications
time.sleep(10)
notifictaions = driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]").click()

# FastAPI
app = FastAPI(title='InstaPy')

@app.get('/', include_in_schema=False)
async def redirect_root():
    return starlette.responses.RedirectResponse('/redoc')

@app.get('/api/v1/searchName')
async def search_name(name: str):
    searchbox = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Search']")
    searchbox.clear()
    searchbox.send_keys(name)
    time.sleep(3)
    users = driver.find_elements(By.XPATH, "//div[@class='_aacl _aaco _aacw _aacx _aad6']")
    usernames = list(map(lambda user: user.text, users))
    return usernames