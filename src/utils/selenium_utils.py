from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from typing import Optional
from unidecode import unidecode


def configure_driver() -> webdriver.Chrome:
    
    """
    Configures and returns a Chrome WebDriver instance with predefined settings.
    """

    options = Options()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-gpu') 
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage') 
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36') 
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--log-level=3")

    return webdriver.Chrome(options=options)


def search_more_filters(
        driver: webdriver,
        variable: str,
        name: str,
        subitems: Optional[bool] = None
        ) -> None:

    """
    Performs Selenium click actions for each filter variable in the website menus.
    
    Parameters:
        driver (webdriver): Selenium WebDriver instance used for browser automation.
        variable (str): Text of the filter option to be matched within the span element.
        name (str): The HTML fieldset name attribute where the filter options are located.
        subitems (Optional[bool]): If True, allows clicking multiple sub-options instead of a single value (e.g., amenities, furniture, accessibility items).
      

    """

    if variable and not subitems:
        field = driver.find_elements(By.XPATH, f'//fieldset[@name="{name}"]//label//div//span[contains(text(), "{variable}")]')[0].click()

    if variable and subitems:
        field = driver.find_elements(By.XPATH, f'//fieldset[@name="{name}"]//label')
        for f in field:
            if 'todos' in variable:
                f.find_element(By.XPATH, 'span[1]').click()
            elif unidecode(f.text.lower()) in variable:
                f.find_element(By.XPATH, 'span[1]').click()