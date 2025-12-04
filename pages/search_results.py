from selenium.webdriver.common.by import By
from .base import BasePage


class SearchResultsPage(BasePage):
    # Title/header that reflects the search term; try common patterns
    RESULTS_TITLE_LOCATORS = [
        (By.CSS_SELECTOR, "h1"),
        (By.CSS_SELECTOR, "h1[class*='title'], h1[class*='Title']"),
        (By.XPATH, "//h1"),
    ]

    # First product link: resilient patterns for product cards
    FIRST_PRODUCT_LINK_LOCATORS = [
        (By.XPATH, "(//a[contains(@href, '/producto/') or contains(@href, '/moda/') or contains(@href, '/deportes/')])[1]"),
        (By.CSS_SELECTOR, "a[data-testid*='product-card']:first-child"),
        (By.CSS_SELECTOR, "article a[href*='/producto/']"),
    ]

    # Brand filter: attempt common filter UI patterns
    BRAND_FILTER_TOGGLE_LOCATORS = [
        (By.XPATH, "//button[contains(., 'Marca') or contains(., 'Marcas')]"),
        (By.CSS_SELECTOR, "button[aria-controls*='brand'], button[aria-label*='Marca']"),
    ]
    BRAND_OPTION_TEMPLATE = "//label[contains(., '{brand}') or //span[contains(., '{brand}')]]"
    APPLY_FILTER_BUTTON_LOCATORS = [
        (By.XPATH, "//button[contains(., 'Aplicar')]"),
        (By.CSS_SELECTOR, "button[type='submit'][class*='apply']"),
    ]

    PRODUCT_GRID_ITEMS_LOCATORS = [
        (By.CSS_SELECTOR, "[data-testid*='product-card']"),
        (By.CSS_SELECTOR, "article[class*='product']"),
        (By.XPATH, "//a[contains(@href, '/producto/')]/ancestor::article"),
    ]

    def get_results_title_text(self) -> str:
        for locator in self.RESULTS_TITLE_LOCATORS:
            try:
                el = self.wait_for_visible(locator)
                return el.text.strip()
            except Exception:
                continue
        raise RuntimeError("Results title not found with available locators.")

    def click_first_product(self):
        for locator in self.FIRST_PRODUCT_LINK_LOCATORS:
            try:
                self.click(locator)
                return
            except Exception:
                continue
        raise RuntimeError("No product link found to click.")

    def open_brand_filter(self):
        for locator in self.BRAND_FILTER_TOGGLE_LOCATORS:
            try:
                self.click(locator)
                return True
            except Exception:
                continue
        return False

    def choose_brand(self, brand_name: str):
        # Use a dynamic XPath to find the brand option
        from selenium.webdriver.common.by import By
        brand_xpath = self.BRAND_OPTION_TEMPLATE.format(brand=brand_name)
        try:
            self.click((By.XPATH, brand_xpath))
            return True
        except Exception:
            return False

    def apply_filter(self):
        for locator in self.APPLY_FILTER_BUTTON_LOCATORS:
            try:
                self.click(locator)
                return True
            except Exception:
                continue
        # Some UIs auto-apply filters on click; returning False is acceptable
        return False

    def count_listed_products(self) -> int:
        # Count by first available locator that yields elements
        for locator in self.PRODUCT_GRID_ITEMS_LOCATORS:
            try:
                elements = self.driver.find_elements(*locator)
                if elements:
                    return len(elements)
            except Exception:
                continue
        # If none found, try waiting for any item and then re-count
        try:
            self.wait_for_visible(self.PRODUCT_GRID_ITEMS_LOCATORS[0])
            elements = self.driver.find_elements(*self.PRODUCT_GRID_ITEMS_LOCATORS[0])
            return len(elements)
        except Exception:
            return 0
