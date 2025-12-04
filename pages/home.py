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
        (By.XPATH, "//form//input[contains(@placeholder, 'buscar') or contains(@placeholder, 'Buscar') or contains(@placeholder, 'search') ]"),
        (By.CSS_SELECTOR, "input[aria-label*='Buscar']"),
        # El Corte Inglés: input dentro de la barra de búsqueda
        (By.CSS_SELECTOR, "input.search-bar__input"),
        (By.XPATH, "//input[@data-synth='LOCATOR_SEARCH_INPUT']"),
        (By.CSS_SELECTOR, "input[placeholder*='¿Qué estás buscando?']"),
    ]

    # Algunos sitios requieren pinchar un botón/trigger para abrir la barra de búsqueda
    SEARCH_BUTTON_LOCATORS = [
        (By.ID, "searchBoxBtn"),
        (By.CSS_SELECTOR, "button[data-testid='SearchBarLink']"),
        (By.CSS_SELECTOR, "button.search-link"),
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
        # Primero intentamos abrir la barra de búsqueda si existe un trigger
        for btn_locator in self.SEARCH_BUTTON_LOCATORS:
            try:
                # No fallamos si no existe; con éxito salimos
                self.click(btn_locator)
                break
            except Exception:
                continue

        # Ahora buscamos el input visible
        search_input = None
        for locator in self.SEARCH_INPUT_LOCATORS:
            try:
                search_input = self.wait_for_visible(locator)
                break
            except Exception:
                continue

        if not search_input:
            raise RuntimeError("Search input not found with available locators.")

        # Asegurarnos de que el input está enfocado y listo
        try:
            # Click para enfocar (algunos inputs requieren focus explícito)
            try:
                search_input.click()
            except Exception:
                pass

            try:
                search_input.clear()
            except Exception:
                pass

            # Enviar la consulta
            search_input.send_keys(query)
            search_input.send_keys(Keys.RETURN)
        except Exception as e:
            raise RuntimeError(f"Failed to type into search input: {e}")

        # Esperar hasta que la URL o el título de resultados reflejen la búsqueda
        try:
            # esperar que el parámetro de búsqueda aparezca en la URL
            self.wait.until(lambda d: query.lower() in d.current_url.lower())
            return True
        except Exception:
            # Si no aparece en la URL, intentar esperar por un título de resultados
            from selenium.webdriver.common.by import By as _By
            from selenium.webdriver.support import expected_conditions as _EC
            try:
                # Esperar un h1 visible y comprobar su texto
                h1 = self.wait.until(_EC.visibility_of_element_located(( _By.CSS_SELECTOR, "h1" )))
                if query.lower() in h1.text.lower():
                    return True
            except Exception:
                pass

        # Si no se detecta navegación ni título, considerar fallo
        raise RuntimeError("Search did not navigate to results or show expected title.")
