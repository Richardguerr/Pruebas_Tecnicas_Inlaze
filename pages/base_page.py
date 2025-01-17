from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator_type, locator_value):

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((locator_type, locator_value))
        )
        
        return self.driver.find_element(locator_type, locator_value)

    def type_text(self, locator_type, locator_value, text):
        # Espera hasta que el elemento sea interactuable
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((locator_type, locator_value))
        )
        element = self.find_element(locator_type, locator_value)
        element.clear()
        element.send_keys(text)

    def click_element(self, locator_type, locator_value):
         # Espera hasta que el elemento sea interactuable
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((locator_type, locator_value))
        )
        
        element = self.find_element(locator_type, locator_value)
        element.click()

    def is_button_submit_enabled(self, locator_type, locator_value):
        try:
            # Esperar a que el botón de login esté presente y sea habilitado
            login_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((locator_type,locator_value))  # Espera a que el botón de login esté presente
            )
            
            # Verificar si el botón está habilitado
            if login_button.is_enabled():
                return True  # El usuario está deslogueado y el botón está habilitado, por lo que se puede loguear nuevamente, por eso retorna False
            else:
                return False  # El botón está presente pero deshabilitado, el usuario esta deslogueado

        except Exception:
            # Si no se encuentra el botón de login, significa que el usuario sigue logueado
            return False
        
    def is_alert_present(self, locator_type, locator_value):
        try:
            # Esperar hasta que la alerta (div con el mensaje) esté presente en el DOM
            alert_element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((locator_type, locator_value))  # Espera hasta que el div esté presente en el DOM
            )
            # Verificar si el mensaje de la alerta es visible
            if alert_element.is_displayed():
                return True  # La alerta está presente y visible
            else:
                return False  # La alerta está presente en el DOM, pero no visible

        except Exception:
            # Si no se encuentra el div con el mensaje de alerta, retorna False
            return False
        
    def wait_for_url_change(self, initial_url, timeout=10):
        """
        Espera hasta que la URL cambie de la URL inicial.
        
        :param driver: Instancia de WebDriver.
        :param initial_url: URL inicial que se está monitoreando.
        :param timeout: Tiempo máximo en segundos para esperar el cambio de URL (default: 10 segundos).
        :return: True si la URL cambió, False si no.
        """
        try:
            # Esperar hasta que la URL cambie
            WebDriverWait(self.driver, timeout).until(EC.url_changes(initial_url))

            # Verificar si la URL ha cambiado
            current_url = self.driver.current_url
            if current_url != initial_url:
                return True
            else:
                return False
        except TimeoutException:
            return False
        
    def is_element_visible(self, *locator):
        try:
            element = self.driver.find_element(*locator)
            return element.is_displayed()
        except Exception:
            return False

    def find_span(self, locator_type, locator_value):

        try:
            WebDriverWait(self.driver, 1).until(
                EC.presence_of_element_located((locator_type, locator_value))
            )
            return True
        except (TimeoutException, NoSuchElementException):
            return False