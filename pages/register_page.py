from selenium.webdriver.common.by import By
# login_page.py
from pages.base_page import BasePage  # Ajusta la importación


class RegisterPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.name_field = (By.ID, "full-name")
        self.email_field = (By.ID, "email")
        self.password_field = (By.XPATH, "//input[@id='password']")
        self.confirm_password_field = (By.XPATH, "//input[@id='confirm-password']")
        self.submit_button = (By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'sign up')]")
        self.alert_locator = (By.CSS_SELECTOR, "div.ml-3.text-sm.font-normal")# Elemento que muestra el nombre del usuario al iniciar sesión
        self.passwords_not_match = (By.CLASS_NAME, "text-error")


    def register_user(self, name, email, password, confirm_password):
        self.type_text(*self.name_field, name)
        self.type_text(*self.email_field, email)
        self.type_text(*self.password_field, password)
        self.type_text(*self.confirm_password_field, confirm_password)
        buton_is_enabled = self.is_button_submit_enabled(*self.submit_button)
        if buton_is_enabled is True:
            self.click_element(*self.submit_button)
            alert_present = self.is_alert_present(*self.alert_locator)
            if alert_present is True:
                return True
            else:
                return False
        else:
            return False
        
    def message_paswords_match(self):
        return self.find_span(*self.passwords_not_match)
