from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver, timeout: int = 15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url: str):
        self.driver.get(url)

    def wait_for_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator):
        element = self.wait_for_clickable(locator)
        element.click()
        return element

    def type_text(self, locator, text: str, clear_first: bool = True):
        element = self.wait_for_visible(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)
        return element

    def get_current_url(self) -> str:
        return self.driver.current_url

    def element_exists(self, locator) -> bool:
        try:
            self.wait_for_visible(locator)
            return True
        except Exception:
            return False
