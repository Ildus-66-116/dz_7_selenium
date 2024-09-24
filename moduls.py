from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
from random import randint
import csv


def write_to_csv(file_path, data):
    """Запись в csv"""
    fieldnames = set()
    for d in data:
        fieldnames.update(d.keys())
    fieldnames = sorted(fieldnames)
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def selenium_hh(query: str):
    """Сбор данным с помощью selenium"""

    options = Options()
    options.add_argument('start-maximized')

    driver = webdriver.Chrome(options=options)
    driver.get('https://hh.ru/')
    data_vacancy = []

    time.sleep(3)
    _input = driver.find_element(By.XPATH, '//input[@id="a11y-search-input"]')
    _input.send_keys(query)
    _input.send_keys(Keys.ENTER)
    actions = ActionChains(driver)
    actions.move_by_offset(100, 100).click().perform()

    wait = WebDriverWait(driver, 30)
    try:
        pages = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@data-qa, "number-pages")]')))
        for page in pages:
            url_page = page.get_attribute('href')
            driver.get(url_page)
            wait = WebDriverWait(driver, 30)
            vacancys = wait.until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "vacancy-info")]')))
            for vacancy in vacancys:
                vacancy_dict = {}
                url_vac = vacancy.find_element(By.XPATH, './/span/a[contains(@class, "magritte-link")]').get_attribute(
                    'href')
                vacancy_dict['link'] = url_vac

                try:
                    pattern = r'/vacancy/(\d+)'
                    match = re.search(pattern, url_vac)
                    _id = int(match.group(1))
                except:
                    _id = randint(1_000_000, 2_000_000)
                vacancy_dict['id'] = _id

                try:
                    price = vacancy.find_element(By.XPATH, './/div[contains(@class, "compensation-labels")]/span').text
                except:
                    price = None
                vacancy_dict['price'] = price

                try:
                    name = vacancy.find_element(By.XPATH, './/span[@data-qa="serp-item__title-text"]').text
                except:
                    name = None
                vacancy_dict['name'] = name
                data_vacancy.append(vacancy_dict)
                print(f'Обработано {len(data_vacancy)} вакансий.')
    except:
        vacancys = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "vacancy-info")]')))
        for vacancy in vacancys:
            vacancy_dict = {}
            url_vac = vacancy.find_element(By.XPATH, './/span/a[contains(@class, "magritte-link")]').get_attribute(
                'href')
            vacancy_dict['link'] = url_vac

            try:
                pattern = r'/vacancy/(\d+)'
                match = re.search(pattern, url_vac)
                _id = int(match.group(1))
            except:
                _id = randint(1_000_000, 2_000_000)
            vacancy_dict['id'] = _id

            try:
                price = vacancy.find_element(By.XPATH, './/div[contains(@class, "compensation-labels")]/span').text
            except:
                price = None
            vacancy_dict['price'] = price

            try:
                name = vacancy.find_element(By.XPATH, './/span[@data-qa="serp-item__title-text"]').text
            except:
                name = None
            vacancy_dict['name'] = name
            data_vacancy.append(vacancy_dict)
            print(f'Обработано {len(data_vacancy)} вакансий.')

    return data_vacancy
