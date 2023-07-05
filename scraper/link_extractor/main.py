from getopt import getopt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
import sys
import datetime


def main():
    now = datetime.datetime.now().timetuple()
    feed_file = f'./links_{now.tm_hour}-{now.tm_min}-{now.tm_sec}.txt'
    start_url = "https://torob.com/browse/99/%D9%84%D9%BE-%D8%AA%D8%A7%D9%BE-%D9%88-%D9%86%D9%88%D8%AA-%D8%A8%D9%88" \
                "%DA%A9-laptop/?stock_status=new"
    count = 24

    opts, _ = getopt(sys.argv[1:], 'o:l:c:', ["output=", "start_url=", "count="])
    for opt, arg in opts:
        if opt in ('-o', '--output'):
            feed_file = arg
        elif opt in ('-l', '--start_url'):
            start_url = arg
        elif opt in ('-c', '--count'):
            count = int(arg)

    extract(feed_file=feed_file, start_url=start_url, count=count)


def extract(feed_file, start_url, count):
    feed = open(feed_file, 'x')

    # Options for the chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')

    # Start the driver.
    print('starting the driver')
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 1)

    print('loading the page')
    driver.get(start_url)

    cards_per_page = 24
    count -= 1
    count = max(count, 1)
    max_retries = 20
    current_retires = 0
    i = 1
    while i <= count // cards_per_page + 1:
        expected_card_count = i * cards_per_page
        print('waiting for total of', expected_card_count)

        try:
            wait.until(ec.presence_of_element_located(
                (By.CSS_SELECTOR, f'.cards > .jsx-fa8eb4b3b47a1d18:nth-child({expected_card_count})')))
            current_retires = 0
        except TimeoutException:
            print('timeout exception')
            i -= 1
            current_retires += 1
            if current_retires == max_retries:
                print('maximum retries reached')
                break

        print('scrolling down')
        driver.execute_script('window.scrollBy(0, 1000)')
        i += 1

    elements = driver.find_elements(By.CSS_SELECTOR, 'a.jsx-fa8eb4b3b47a1d18')
    for link in elements:
        feed.write(link.get_attribute('href'))
        feed.write('\n')


if __name__ == "__main__":
    main()
