from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement
from typing import Optional
from time import sleep


def button_next(
        driver: webdriver.Chrome
        ) -> Optional[WebElement]:
    
    """
    Attempts to click the "Ver mais" button on the QuintoAndar results page.

    Parameters:
        driver (webdriver.Chrome): The active Selenium Chrome WebDriver instance.
    """
    
    wait = WebDriverWait(driver, 10)

    try:
        button_ver_mais = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="load-more-button"]')))
        driver.execute_script('arguments[0].scrollIntoView({block: "center"});', button_ver_mais)
        sleep(0.1)
        button_ver_mais.click()
        sleep(1.2)

        return button_ver_mais

    except StaleElementReferenceException:
        print('Sem mais botões na tela!')
        return None

    except TimeoutException:
        print("Tempo finalizado!")
        return None

    
    
        
    
    