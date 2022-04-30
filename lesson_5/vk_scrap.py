from time import sleep
import requests

from lxml.html import fromstring
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


def search_posts(search_text):
    search_button = driver.find_element_by_xpath("//a[contains(@class, 'ui_tab_plain ui_tab_search')]")
    search_button.click()
    sleep(1)
    search_field = driver.find_element_by_id("wall_search")
    search_field.clear()
    search_field.send_keys(search_text + Keys.ENTER)
    search_field.is_enabled()


def auth_box():
    sleep(1)
    unauth_box = driver.find_elements_by_class_name("UnauthActionBox__close")
    if unauth_box:
        unauth_box[0].click()


URL = "https://vk.com/tokyofashion"
DRIVER_PATH = "./selenium_drivers/chromedriver"
MAX_PAGE_NUMBER = 5

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(DRIVER_PATH, options=options)

driver.get(URL)
sleep(3)
search_posts("юбка")
sleep(3)

# response = requests.get(URL)
# dom = fromstring(response.text)


posts = driver.find_elements_by_class_name("post_info")
actions = ActionChains(driver)
actions.move_to_element(posts[-1])
# actions.send_keys(Keys.END)
sleep(2)
# auth_box()


print()
