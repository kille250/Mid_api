import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class tlogin():
    def __init__(self):
        self.url = "http://127.0.0.1:5000"

        self.elements_check = [
            "//input[@name='lname']",
            "//input[@name='lpassword']",
            "//input[@value='Submit']"
            ]

    def login_check_elements(self, driver):
        wait = WebDriverWait(driver, 10)

        for i in self.elements_check:
            wait.until(
                EC.presence_of_element_located((By.XPATH, i))
                )
        return wait

    def login_wrong_creditals(self):
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(self.url)

        wait = self.login_check_elements(driver)

        driver.find_element(By.XPATH, "//input[@name='lname']").send_keys("Test")
        driver.find_element(By.XPATH, "//input[@name='lpassword']").send_keys("test")
        driver.find_element(By.XPATH, "//input[@value='Submit']").click()

        wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'alert')]"))
        )
        print("Working")

        driver.close()


if __name__ == "__main__":
    tlogin = tlogin()
    tlogin.login_wrong_creditals()
