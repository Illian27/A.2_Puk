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
        # Cerrar modal si aparece tras la búsqueda
        try:
            self.close_modal_if_present()
        except Exception:
            pass

        # Intento 1: localizar un h1 habitual
        for locator in self.RESULTS_TITLE_LOCATORS:
            try:
                el = self.wait_for_visible(locator)
                text = el.text.strip()
                if text:
                    return text
            except Exception:
                continue

        # Intento 2: esperar a que aparezcan elementos de producto y revisar el título de la página
        try:
            for prod_locator in self.PRODUCT_GRID_ITEMS_LOCATORS:
                try:
                    # esperar hasta que haya al menos un elemento de producto
                    self.wait.until(lambda d, l=prod_locator: len(d.find_elements(*l)) > 0)
                    break
                except Exception:
                    continue
        except Exception:
            pass

        # Intento 3: usar el título de la página (document.title)
        try:
            page_title = (self.driver.title or "").strip()
            if page_title:
                return page_title
        except Exception:
            page_title = ""

        # Intento 4: extraer el valor del input de búsqueda (a veces refleja el término)
        try:
            el = self.driver.find_element(By.CSS_SELECTOR, "input.search-bar__input")
            val = (el.get_attribute("value") or el.get_attribute("placeholder") or "").strip()
            if val:
                return val
        except Exception:
            pass

        # Intento 5: parsear la URL en busca de parámetros de búsqueda
        try:
            from urllib.parse import urlparse, parse_qs
            parsed = urlparse(self.driver.current_url)
            qs = parse_qs(parsed.query)
            for key in ("q", "query", "search", "s"):
                if key in qs and qs[key]:
                    return qs[key][0]
            # también buscar en la ruta segmentos que parezcan el término
            path_parts = [p for p in parsed.path.split('/') if p]
            if path_parts:
                # tomar el último segmento legible
                last = path_parts[-1]
                if last and not last.isnumeric():
                    return last.replace('-', ' ')
        except Exception:
            pass

        # Intento 6: extraer nombre del primer producto o marca visible
        product_title_selectors = [
            "[itemprop='name']",
            "h3[class*='title']",
            "h3[class*='product']",
            "p.product_preview-brand--text",
            "a[data-testid*='product-card']",
            "article[class*='product']",
        ]
        try:
            for sel in product_title_selectors:
                try:
                    els = self.driver.find_elements(By.CSS_SELECTOR, sel)
                    for e in els:
                        txt = (e.text or e.get_attribute('innerText') or '').strip()
                        if txt:
                            return txt
                except Exception:
                    continue
        except Exception:
            pass

        # No hemos conseguido detectar el título; devolver información de depuración
        snippet = ""
        try:
            snippet = self.driver.page_source[:1000]
        except Exception:
            pass
        raise RuntimeError(f"Results title not found with available locators. page_title='{page_title}' snippet='{snippet[:200]}' url='{self.driver.current_url}'")

    def click_first_product(self):
        # A veces un modal bloquea la interacción; intentar cerrarlo primero
        try:
            self.close_modal_if_present()
        except Exception:
            pass

        for locator in self.FIRST_PRODUCT_LINK_LOCATORS:
            try:
                self.click(locator)
                return
            except Exception:
                continue
        raise RuntimeError("No product link found to click.")

    def open_brand_filter(self):
        # Cerrar modal si aparece
        try:
            self.close_modal_if_present()
        except Exception:
            pass

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
        # Cerrar modal si aparece y bloquea las tarjetas
        try:
            self.close_modal_if_present()
        except Exception:
            pass

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
