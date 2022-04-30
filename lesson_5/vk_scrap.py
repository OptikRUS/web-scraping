from pprint import pprint
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from save_posts import save_posts


def search_posts(search_text):
    search_button = driver.find_element_by_xpath("//a[contains(@class, 'ui_tab_plain ui_tab_search')]")
    search_button.click()
    sleep(1)
    search_field = driver.find_element_by_id("wall_search")
    search_field.clear()
    search_field.send_keys(search_text + Keys.ENTER)


def auth_box():
    sleep(1)
    unauth_box = driver.find_elements_by_class_name("UnauthActionBox__close")
    if unauth_box:
        unauth_box[0].click()


def scrap_posts():
    sleep(2)
    posts = driver.find_elements_by_class_name("post_info")
    actions = ActionChains(driver)
    actions.move_to_element(posts[-1])
    actions.perform()
    auth_box()
    return BeautifulSoup(driver.page_source, "html.parser")


def get_elements(scroll_count):
    all_elements = None
    for i in range(scroll_count):
        all_elements = scrap_posts().find_all('div', attrs={'class': '_post_content'})
    return all_elements


URL = "https://vk.com/tokyofashion"
DRIVER_PATH = "./selenium_drivers/chromedriver"
MAX_SCROLL_COUNT = 5

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(DRIVER_PATH, options=options)

driver.get(URL)
sleep(3)
search_posts("юбка")
sleep(3)

elements = get_elements(MAX_SCROLL_COUNT)

for element in elements:
    info = {}
    teg_a = element.find('a', attrs={'class': 'post_link'})
    likes = element.find('div', attrs={'data-section-ref': 'reactions-button'})
    shares = element.find('div', attrs={'class': 'PostBottomAction PostBottomAction--withBg share _share'})
    post_text = element.find('div', attrs={'class': 'wall_post_text'})

    if teg_a and likes and shares and post_text:
        info['url'] = "https://vk.com" + teg_a['href']
        info['date'] = teg_a.span.text
        info['likes'] = int(likes.text)
        info['shares'] = int(shares.text)
        info['text'] = post_text.text
        save_posts(info)
        pprint(info)
