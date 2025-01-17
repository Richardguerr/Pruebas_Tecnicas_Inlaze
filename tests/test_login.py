from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from config import EMAIL, EMAIL_INVALID, PASSWORD, PASSWORD_INVALID, CHROME_DRIVER_PATH  # Importar las variables globales
from selenium.webdriver.common.keys import Keys


# Configuración del servicio
service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service)

# URL de prueba
base_url = "https://test-qa.inlaze.com/"  # Actualiza con la URL real
driver.get(base_url)

# Crear una instancia de la página de login
login_page = LoginPage(driver)


def navigate_to_base_url():
    driver.get(base_url)

# 1. Verificar que el usuario pueda loguearse con el email y contraseña correctos.
def test_login_successful():
    try:
        navigate_to_base_url()  # Navegar a la URL base antes de ejecutar el test
        
        login_successful = login_page.login(EMAIL, PASSWORD)  # Iniciar sesión usando las variables globales
        # Esperar hasta que el nombre de usuario esté visible
        assert login_successful, "Test loging: Usuario no pudo iniciar sesión correctamente."
        print(f"Test loging: Usuario loggeado correctamente ")  
    except AssertionError as e:
        print(f"Test loging: Usuario no pudo iniciar sesión correctamente.")
    except Exception as e:
        print(f"Test de login exitoso: ERROR inesperado.")


# 2. Validar que el formulario de login no se envíe si los campos no están completos.
def test_login_form_empty_fields():
    try:
        navigate_to_base_url()  # Navegar a la URL base antes de ejecutar el test
        login_successful = login_page.login(EMAIL_INVALID, PASSWORD_INVALID)  # Iniciar sesión usando las variables globales
        assert login_successful, "Test campos incompletos: Usuario no pudo iniciar sesión correctamente."
        print(f"Test campos incompletos: Usuario loggeado correctamente ")
        
    except AssertionError as e:
         print(f"Test campos incompletos: Usuario no se loggeo correctamente ")
    except Exception as e:
        print(f"Test de formulario vacío: ERROR inesperado. Error: {e}")


# 3. Comprobar que al ingresar se muestre el nombre del usuario.
def test_user_name_displayed_after_login():
    """
    Prueba que el nombre de usuario se muestre correctamente después de iniciar sesión.
    """
    try:
        # Navegar a la URL base antes de ejecutar el test
        navigate_to_base_url()

        # Intentar iniciar sesión usando las credenciales
        login_is_successful = login_page.login(EMAIL, PASSWORD)

        # Verificar si el inicio de sesión fue exitoso
        if not login_is_successful:
            raise Exception("El usuario no pudo iniciar sesión correctamente.")

        # Verificar que el nombre del usuario esté visible después de iniciar sesión
        user_name = login_page.get_logged_in_user_name()
        assert user_name, "El nombre de usuario no se muestra después de iniciar sesión."

        # Imprimir el resultado exitoso del test
        print(f"Test de nombre de usuario mostrado: ÉXITO. Nombre de usuario: {user_name}")

    except AssertionError as e:
        print(f"Test de nombre de usuario mostrado: FALLIDO. Error: {e}")
    except Exception as e:
        print(f"Test de nombre de usuario: {e}")



# 4. Verificar que la plataforma permita cerrar la sesión correctamente.
def test_logout_functionality():
    """
    Verifica que la plataforma permita cerrar sesión correctamente.
    """
    try:
        # Navegar a la URL base antes de ejecutar el test
        navigate_to_base_url()

        # Intentar iniciar sesión con las credenciales
        login_is_successful = login_page.login(EMAIL, PASSWORD)

        # Verificar si el inicio de sesión fue exitoso
        if not login_is_successful:
            raise Exception("El usuario no pudo iniciar sesión correctamente.")

        # Intentar cerrar sesión
        logout_is_successful = login_page.logout()

        # Verificar si el usuario fue redirigido correctamente después de cerrar sesión
        assert logout_is_successful, "El usuario no fue desconectado correctamente."

        # Si todo es exitoso, imprimir un mensaje de éxito
        print("Test de cierre de sesión: PASADO")
    except AssertionError as e:
        print(f"Test de cierre de sesión: FALLADO. Error: {e}")
    except Exception as e:
        print(f"Test de cierre de sesión: {e}")



# Ejecutar los tests
try:
    test_login_successful()
    test_login_form_empty_fields()
    test_user_name_displayed_after_login()
    test_logout_functionality()
   
finally:
    # Cerrar el navegador
    driver.quit()
