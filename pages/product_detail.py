from selenium.webdriver.common.by import By
from .base import BasePage


class ProductDetailPage(BasePage):
    # Evidence we are on a product detail page
    DETAIL_INDICATORS = [
        (By.CSS_SELECTOR, "h1[itemprop='name'], h1[class*='product']"),
        (By.CSS_SELECTOR, "button[id*='add-to-cart'], button[class*='addToCart']"),
        (By.XPATH, "//section[contains(@class, 'product-detail')]"),
    ]

    def is_on_product_detail(self) -> bool:
        for locator in self.DETAIL_INDICATORS:
            if self.element_exists(locator):
                return True
        return False
