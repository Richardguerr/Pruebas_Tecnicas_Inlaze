# login_page.py
from selenium.webdriver.common.by import By
# login_page.py
from pages.base_page import BasePage  # Ajusta la importación
from selenium.common.exceptions import NoSuchElementException


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.email_field = (By.XPATH, "//input[@type='email']")
        self.password_field = (By.XPATH, "//input[@type='password']")
        self.submit_button = (By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'sign in')]")
        self.logout_button = (By.XPATH, "//a[text()='Logout']")
        self.user_name_display = (By.XPATH, "//h2[@class='font-bold']")
        self.label_button = (By.CSS_SELECTOR, "label[tabindex='0']")  
        self.alert_locator = (By.CSS_SELECTOR, "div.ml-3.text-sm.font-normal")# Elemento que muestra el nombre del usuario al iniciar sesión

    
    
    def login(self, email, password):
    
        self.type_text(*self.email_field, email)
        self.type_text(*self.password_field, password)
        
       
        buton_is_enabled = self.is_button_submit_enabled(*self.submit_button)
        if buton_is_enabled is True:
            self.click_element(*self.submit_button)
            alert_present = self.is_alert_present(*self.alert_locator)
            if alert_present is True:
                return False
            else:
                return True
        else:
            return False

    def logout(self):
        try:
            # Haz clic en el botón para abrir el menú
            self.click_element(*self.label_button)

            # Haz clic en el botón de cerrar sesión
            self.click_element(*self.logout_button)

            # Verifica si el usuario fue redirigido correctamente a la página de inicio de sesión
            return self.is_element_visible(*self.submit_button)
        except Exception as e:
            print(f"Error al cerrar sesión: {e}")
            return False

    
    def get_logged_in_user_name(self):
                return self.find_element(*self.user_name_display).text

    def is_user_logged_ou(self):
        return self.is_button_submit_enabled(*self.submit_button)
    
    def is_url_different(self, initial_url):
            return self.wait_for_url_change(initial_url)
    