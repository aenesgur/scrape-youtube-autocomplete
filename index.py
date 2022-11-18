import re, json, time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from parsel import Selector

search_items = ["rihanna ", "lana del rey ", "eminem "]
youtube_url = "https://www.youtube.com/"
autocomplete_results = []

def scrape_youtube():
    chrome_driver= Service(ChromeDriverManager().install())
    options = get_options()
    for item in search_items:

       execute_scraping(chrome_driver=chrome_driver, options=options, item=item) 
        
    print(json.dumps(autocomplete_results, indent=4))

def get_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('--lang=en')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36")
    return options

def get_driver_settings(chrome_driver, options):
    driver = webdriver.Chrome(service=chrome_driver, options=options)
    driver.get(youtube_url)
    return driver   

def execute_scraping(chrome_driver, options, item):
    driver = get_driver_settings(chrome_driver=chrome_driver, options=options)

    WebDriverWait(driver, 10000).until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))
    
    send_keys(driver=driver, item=item)
    
    time.sleep(1)
    
    cssSelector = Selector(driver.page_source)

    results = get_autocomplete_result(cssSelector=cssSelector)
    
    append_list_autocomplete_results(item=item, results=results)

    finish_driver(driver=driver)

def send_keys(driver, item):
    searchItem = driver.find_element(By.XPATH, '//input[@id="search"]')
    searchItem.click()
    searchItem.send_keys(item)
    
def get_autocomplete_result(cssSelector):
    results = [
            re.search(r'">(.*)</b>', result).group(1).replace("<b>", "")
            for result in cssSelector.css('.sbqs_c').getall()
        ]
    return results

def append_list_autocomplete_results(item, results):
    autocomplete_results.append({
            "item": item.strip(),
            "autocomplete_results": results
        })

def finish_driver(driver):
    driver.quit()
    
scrape_youtube()