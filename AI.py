import selenium
import selenium.webdriver
import time
from selenium.webdriver.common.by import By
import random
import string
import g4f


def random_letters_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def TTM(text):
    driver = selenium.webdriver.Chrome()

    driver.get("https://deepai.org/machine-learning-model/cute-creature-generator")
    driver.maximize_window()


    button = driver.find_element(By.XPATH, '/html/body/main/div[2]/div/div/div[1]/span/textarea')
    button.send_keys(text)


    button = driver.find_element(By.XPATH, '//*[@id="modelSubmitButton"]')
    button.click()

    button = driver.find_element(By.XPATH, '//*[@id="switch-to-email"]')
    button.click()


    time.sleep(0.5)

    button = driver.find_element(By.XPATH, '//*[@id="user-email"]')
    button.send_keys(f"{random_letters_string(10)}@proton.me")


    password = random_letters_string(10)
    button = driver.find_element(By.XPATH, '//*[@id="user-password"]')
    button.send_keys(password)

    button = driver.find_element(By.XPATH, '//*[@id="confirm-user-password"]')
    button.send_keys(password)

    button = driver.find_element(By.XPATH, '//*[@id="login-via-email-id"]')
    button.click()
    time.sleep(5)

    button = driver.find_element(By.XPATH, '//*[@id="modelSubmitButton"]')
    button.click()
    time.sleep(7)

    button = driver.find_element(By.XPATH, '//*[@id="place_holder_picture_model"]/img')
    image_url = button.get_attribute("src")

    return image_url

def gbt(prmt):
 
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        provider=g4f.Provider.FlowGpt,
        messages=[{"role": "user", "content": prmt}],
        
    )

    return response
