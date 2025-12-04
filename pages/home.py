from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base import BasePage


class HomePage(BasePage):
    BASE_URL = "https://www.elcorteingles.es/"

    # Cookie locators: multiple strategies to be resilient
    ACCEPT_COOKIES_BUTTONS = [
        (By.XPATH, "//button[contains(translate(., 'ACEPTAR', 'aceptar'), 'aceptar')]"),
        (By.XPATH, "//button[contains(., 'Aceptar')]"),
        (By.XPATH, "//button[contains(., 'Accept')]"),
        (By.CSS_SELECTOR, "button#onetrust-accept-btn-handler"),  # common OneTrust id
        (By.CSS_SELECTOR, "button[aria-label*='Aceptar']"),
    ]

    # Search input locators: generic search input strategies
    SEARCH_INPUT_LOCATORS = [
        (By.CSS_SELECTOR, "input[type='search']"),
        (By.CSS_SELECTOR, "input[name='q']"),
        (By.XPATH, "//form//input[contains(@placeholder, 'buscar') or contains(@placeholder, 'Buscar') or contains(@placeholder, 'search')]"),
        (By.CSS_SELECTOR, "input[aria-label*='Buscar']"),
    ]

    def go_to_home(self):
        self.open(self.BASE_URL)

    def accept_cookies_if_present(self):
        for locator in self.ACCEPT_COOKIES_BUTTONS:
            try:
                self.click(locator)
                return True
            except Exception:
                continue
        # If none clicked, assume no banner or already accepted
        return False

    def search(self, query: str):
        search_input = None
        for locator in self.SEARCH_INPUT_LOCATORS:
            try:
                search_input = self.wait_for_visible(locator)
                break
            except Exception:
                continue

        if not search_input:
            raise RuntimeError("Search input not found with available locators.")

        search_input.clear()
        search_input.send_keys(query)
        search_input.send_keys(Keys.ENTER)
