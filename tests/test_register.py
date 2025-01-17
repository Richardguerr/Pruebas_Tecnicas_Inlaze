import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from pages.register_page import RegisterPage
from config import CHROME_DRIVER_PATH
import re
from config import EMAIL, EMAIL_INVALID, PASSWORD, PASSWORD_INVALID, CHROME_DRIVER_PATH,USERNAME # Importar las variables globales

# Configuración del servicio
service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service)
# Lista para almacenar los emails existentes
existing_emails = []

# URL de prueba
base_url = "https://test-qa.inlaze.com/auth/sign-up/"  

# Iniciar prueba
driver.get(base_url)
register_page = RegisterPage(driver)

def navigate_to_base_url():
    driver.get(base_url)

def test_valid_user_registration():
    """
    Prueba que un usuario pueda registrarse con datos válidos y no válidos.
    """
    try:

        # Generar datos de prueba
        test_cases = [
            # Caso válido
            {
                "username": "Carlos Martínez",
                "email": "carlos.martinez@example.com",
                "password": "Contraseña12!",
                "confirm_password": "Contraseña12!",
                "expected": True,
                "error": None
            },
            # Caso inválido: Nombre con una sola palabra
            {
                "username": "Juan",
                "email": "juan.doe@example.com",
                "password": "Contraseña12!",
                "confirm_password": "Contraseña12!",
                "expected": False,
                "error": "El nombre debe contener al menos dos palabras."
            },
            # Caso inválido: Email mal formateado
            {
                "username": "Ana López",
                "email": "ana.lopezcom",  # Email sin el "@" y ".com"
                "password": "Contraseña12!",
                "confirm_password": "Contraseña12!",
                "expected": False,
                "error": "El formato del email es incorrecto."
            },
            # Caso inválido: Contraseña demasiado corta
            {
                "username": "Pedro García",
                "email": "pedro.garcia@example.com",
                "password": "Pass123",  # Contraseña corta
                "confirm_password": "Pass123",
                "expected": False,
                "error": "La contraseña debe tener al menos 8 caracteres."
            },
            # Caso inválido: Contraseña excede el límite de caracteres
            {
                "username": "Laura Pérez",
                "email": "laura.perez@example.com",
                "password": "ContraseñaMuyLarga123",  # Contraseña de más de 14 caracteres
                "confirm_password": "ContraseñaMuyLarga123",
                "expected": False,
                "error": "La contraseña no debe exceder los 14 caracteres."
            },
            # Caso inválido: Las contraseñas no coinciden
            {
                "username": "Sofía Ruiz",
                "email": "sofia.ruiz@example.com",
                "password": "Contraseña12!",
                "confirm_password": "Contraseña321!",  # Contraseñas no coinciden
                "expected": False,
                "error": "Las contraseñas no coinciden."
            }
        ]

        # Ejecutar los casos de prueba
        for case in test_cases:

            navigate_to_base_url()
            username = case["username"]
            email = case["email"]
            password = case["password"]
            confirm_password = case["confirm_password"]
            expected = case["expected"]
            error_message = case["error"]

            # Intentar registrar usuario
            register_is_successful = register_page.register_user(username, email, password, confirm_password)
            # Validar si el resultado coincide con lo esperado
            if register_is_successful != expected:
                assert register_is_successful != expected, f" - Error esperado: {error_message}"
                print(f"Test de registro -> FALLIDO, Esperado: {expected}, Obtenido: {register_is_successful} , - Error esperado: {error_message}")
               

            else:
                assert register_is_successful == expected, f" - Error esperado: {error_message}"
                print(f"Test de registro -> ÉXITOSO: Esperado: {expected}, Obtenido: {register_is_successful}, - Error esperado: {error_message}")

    except AssertionError as e:
        print(f"Test de registro -> FALLIDO.  {e}")
    except Exception as e:
        print(f"Test de registro: ERROR inesperado. Detalle: {e}")


def test_user_name_minimum_two_words():
    """
    Prueba que el campo de nombre de usuario contenga al menos dos palabras (primer nombre y apellido).
    """
    try:
        # Generar datos de prueba
        test_cases = [
            # Caso válido
            {
                "username": "Carlos Martínez",  # Nombre con dos palabras
                "expected": True,
                "error": None
            },
            # Caso inválido: Nombre con una sola palabra
            {
                "username": "Juan",  # Nombre con una sola palabra
                "expected": False,
                "error": "El nombre debe contener al menos dos palabras (primer nombre y apellido)."
            },
            # Caso inválido: Nombre con más de dos palabras
            {
                "username": "Juan Carlos Martínez",  # Nombre con más de dos palabras
                "expected": True,
                "error": None
            }
        ]

        # Ejecutar los casos de prueba
        for case in test_cases:
            navigate_to_base_url()
            username = case["username"]
            expected = case["expected"]
            error_message = case["error"]

            # Intentar registrar usuario
            register_is_successful = register_page.register_user(username, EMAIL, PASSWORD, PASSWORD)
            
            # Verificar si el resultado coincide con lo esperado
            if register_is_successful != expected:
                assert register_is_successful != expected, f" - Error esperado: {error_message}"
                print(f"Test de Nombre de Usuario: {username} -> FALLIDO,  Esperado: {expected}, Obtenido: {register_is_successful} , - Error esperado: {error_message}")
               

            else:
                assert register_is_successful == expected, f" - Error esperado: {error_message}"
                print(f"Test de Nombre de Usuario: {username} -> ÉXITOSO: Esperado: {expected}, Obtenido: {register_is_successful}, - Error esperado: {error_message}")

    except Exception as e:
        print(f"Test de registro: ERROR inesperado. Detalle: {e}")

def test_email_format_and_uniqueness():
    """
    Prueba que el campo de email cumpla con el formato estándar y que sea único en la base de datos.
    """
    try:
        # Generar datos de prueba
        test_cases = [
            # Caso válido: Email con formato correcto y único
            {
                "email": "usuario@example.com",  # Email válido
                "expected_format": True,
                "expected_unique": True,
                "error": None
            },
            # Caso inválido: Email mal formateado
            {
                "email": "usuario@example",  # Email sin el dominio adecuado
                "expected_format": False,
                "expected_unique": True,  # La unicidad es irrelevante si el formato es incorrecto
                "error": "El formato del email es incorrecto."
            },
            # Caso inválido: Email repetido (no único)
            {
                "email": "usuario@example.com",  # Email que ya existe en la base de datos
                "expected_format": True,
                "expected_unique": False,
                "error": "El email ya está registrado."
            }
        ]


        # Ejecutar los casos de prueba
        for case in test_cases:
            navigate_to_base_url()
            email = case["email"]
            expected_format = case["expected_format"]
            expected_unique = case["expected_unique"]
            error_message = case["error"]

            # Verificar el formato del email
            email_format_is_valid = bool(re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email))

            # Verificar si el email ya existe en la base de datos (simulando la consulta)
            email_is_unique = check_email_uniqueness(email)
            register_is_successful = register_page.register_user(USERNAME, email, PASSWORD, PASSWORD)

      
            try:
                assert email_format_is_valid == expected_format, f" - Error esperado: {error_message} (Formato)"
                assert email_is_unique == expected_unique, f" - Error esperado: {error_message} (Unicidad)"
                
                result_status = "ÉXITOSO" if expected_format and expected_unique and register_is_successful else "FALLIDO"
                print(f"Test de email: {email} -> {result_status}: Formato esperado: {expected_format}, Unicidad esperada: {expected_unique}, Obtenido: Formato: {email_format_is_valid}, Unicidad: {email_is_unique} - Error esperado: {error_message}")
            except AssertionError:
                print(f"Test de email: {email} -> FALLIDO. Formato esperado: {expected_format}, Unicidad esperada: {expected_unique}, Obtenido: Formato: {email_format_is_valid}, Unicidad: {email_is_unique} - Error esperado: {error_message}")
                continue  # Opcional: Para continuar con el siguiente caso

    except Exception as e:
        print(f"Test de email: ERROR inesperado. Detalle: {e}")

def check_email_uniqueness(email):
    """
    Función simulada para verificar la unicidad del email en la base de datos.
    (En un caso real, esto debería consultar la base de datos).
    """
    # Verificar si el email ya está en la lista antes de añadirlo
    if email in existing_emails:
        return False  # El email no es único
    
    # Si el email no está en la lista, lo añadimos
    existing_emails.append(email)
    return True  # El email es único



def test_password_validity():
    """
    Prueba que la contraseña cumpla con los requisitos de longitud y caracteres.
    """
    try:
        # Generar datos de prueba
        test_cases = [
            # Caso válido: Contraseña que cumple con todos los requisitos
            {
                "password": "Contraseña12!",  # Longitud entre 8 y 14, tiene mayúsculas, minúsculas, números y caracteres especiales
                "expected": True,
                "error": None
            },
            # Caso inválido: Contraseña demasiado corta
            {
                "password": "Pass1!",  # Menos de 8 caracteres
                "expected": False,
                "error": "La contraseña debe tener al menos 8 caracteres."
            },
            # Caso inválido: Contraseña demasiado larga
            {
                "password": "ContraseñaMuyLarga123!",  # Más de 14 caracteres
                "expected": False,
                "error": "La contraseña no debe exceder los 14 caracteres."
            },
            # Caso inválido: Contraseña sin caracteres especiales
            {
                "password": "Contraseña123",  # Falta el carácter especial
                "expected": False,
                "error": "La contraseña debe contener al menos un carácter especial."
            },
            # Caso inválido: Contraseña sin número
            {
                "password": "Contraseña!",  # Falta un número
                "expected": False,
                "error": "La contraseña debe contener al menos un número."
            },
            # Caso inválido: Contraseña sin mayúsculas
            {
                "password": "contraseña12!",  # Falta una mayúscula
                "expected": False,
                "error": "La contraseña debe contener al menos una letra mayúscula."
            },
            # Caso inválido: Contraseña sin minúsculas
            {
                "password": "CONTRASEÑA12!",  # Falta una minúscula
                "expected": False,
                "error": "La contraseña debe contener al menos una letra minúscula."
            }
        ]

        
        # Ejecutar los casos de prueba
        for case in test_cases:
            navigate_to_base_url()
            password = case["password"]
            expected = case["expected"]
            error_message = case["error"]

            # Verificar si la contraseña cumple con los requisitos
            password_is_valid = validate_password(password)
            register_is_successful = register_page.register_user(USERNAME, EMAIL, password, password)
            # Verificar si el resultado coincide con lo esperado
            try:
                assert password_is_valid == expected, f" - Error esperado: {error_message}"
                result_status = "ÉXITOSO" if expected == register_is_successful else "FALLIDO"
                print(f"Test de contraseña: {password} -> {result_status}: Esperado: {expected}, Obtenido: {register_is_successful} - Error esperado: {error_message}")
            except AssertionError:
                print(f"Test de contraseña: {password} -> FALLIDO. Esperado: {expected}, Obtenido: {register_is_successful} - Error esperado: {error_message}")
                continue  # Opcional: Para continuar con el siguiente caso

    except Exception as e:
        print(f"Test de contraseña: ERROR inesperado. Detalle: {e}")


def test_form_submission():
    """
    Prueba que el formulario no sea enviado si hay campos obligatorios incompletos.
    """
    test_cases = [
        # Caso válido: Todos los campos están completos
        {
            "form_data": {
                "username": "Carlos Martínez",
                "email": "carlos.martinez@example.com",
                "password": "Contraseña12!",
                "confirm_password": "Contraseña12!"
            },
            "expected": True,
            "error_message": None
        },
        # Caso inválido: Campo 'username' vacío
        {
            "form_data": {
                "username": "",
                "email": "ana.lopez@example.com",
                "password": "Contraseña12!",
                "confirm_password": "Contraseña12!"
            },
            "expected": False,
            "error_message": "El campo 'username' es obligatorio."
        },
        # Caso inválido: Campo 'email' vacío
        {
            "form_data": {
                "username": "Ana López",
                "email": "",
                "password": "Contraseña12!",
                "confirm_password": "Contraseña12!"
            },
            "expected": False,
            "error_message": "El campo 'email' es obligatorio."
        },
        # Caso inválido: Campo 'password' vacío
        {
            "form_data": {
                "username": "Pedro García",
                "email": "pedro.garcia@example.com",
                "password": "",
                "confirm_password": "Contraseña12!"
            },
            "expected": False,
            "error_message": "El campo 'password' es obligatorio."
        },
        # Caso inválido: Las contraseñas no coinciden
        {
            "form_data": {
                "username": "Sofía Ruiz",
                "email": "sofia.ruiz@example.com",
                "password": "Contraseña12!",
                "confirm_password": "Contraseña123!"
            },
            "expected": False,
            "error_message": "Las contraseñas no coinciden."
        }
    ]

    for case in test_cases:
        navigate_to_base_url()
        form_data = case["form_data"]
        expected = case["expected"]
        error_message = case["error_message"]

        is_valid, errors = validate_form(form_data)
        register_is_successful = register_page.register_user(form_data["username"], form_data["email"], form_data["password"], form_data["confirm_password"])

        try:
            assert is_valid == expected and is_valid == register_is_successful, f"Error esperado: {error_message}, obtenido: {errors}"
            print(f"Test de formulario: {form_data} -> ÉXITOSO: Esperado: {expected}, Obtenido: {is_valid}")
        except AssertionError:
            print(f"Test de formulario: {form_data} -> FALLIDO: Esperado: {expected}, Obtenido: {is_valid} - Detalles: {errors}")


def test_password_match():
    """
    Prueba la validación de la coincidencia de contraseñas.
    """
    test_cases = [
        # Caso válido: Las contraseñas coinciden
        {
            "password": "Contraseña1!",
            "confirm_password": "Contraseña1!",
            "expected": True,
            "message": "Las contraseñas coinciden."
        },
        # Caso inválido: Las contraseñas no coinciden
        {
            "password": "Contraseña1!",
            "confirm_password": "ContraseñaDiferente2!",
            "expected": False,
            "message": "Las contraseñas no coinciden. Por favor, verifica ambas."
        },
        # Caso inválido: Una contraseña está vacía
        {
            "password": "Contraseña1!",
            "confirm_password": "",
            "expected": False,
            "message": "Las contraseñas no coinciden. Por favor, verifica ambas."
        }
    ]

    for case in test_cases:
        navigate_to_base_url()
        password = case["password"]
        confirm_password = case["confirm_password"]
        expected = case["expected"]
        expected_message = case["message"]

        result, message = validate_password_match(password, confirm_password)
        register_page.register_user(USERNAME, EMAIL, password, confirm_password);

        try:
            assert result == expected, f"Esperado: {expected}, Obtenido: {result}"
            assert register_page.message_paswords_match() is False, f"Mensaje esperado: '{expected_message}', Obtenido: '{message}'"
            print(f"Test de validación de contraseñas: {password}, {confirm_password} -> ÉXITOSO: {message}")
        except AssertionError as e:
            print(f"Test de validación de contraseñas: {password}, {confirm_password} -> FALLIDO: {e}")

def validate_password(password):
    """
    Función para validar la contraseña según los siguientes criterios:
    - Longitud mínima de 8 caracteres y máxima de 14 caracteres.
    - Debe contener al menos una letra mayúscula.
    - Debe contener al menos una letra minúscula.
    - Debe contener al menos un número.
    - Debe contener al menos un carácter especial (ej. !, @, #, $, etc.).
    """
    # Longitud de la contraseña
    if len(password) < 8 or len(password) > 14:
       
        return False

    # Verificar mayúsculas, minúsculas, números y caracteres especiales
    if not re.search(r"[A-Z]", password):  # Al menos una mayúscula
     
        return False

    if not re.search(r"[a-z]", password):  # Al menos una minúscula
      
        return False

    if not re.search(r"\d", password):  # Al menos un número
    
        return False

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):  # Al menos un carácter especial
       
        return False

    return True

def validate_form(form_data):
    """
    Verifica que todos los campos obligatorios del formulario estén completos.

    Args:
        form_data (dict): Un diccionario con los datos del formulario. Cada clave representa
                          un campo del formulario y el valor es el contenido del campo.

    Returns:
        bool: True si todos los campos están completos, False en caso contrario.
        list: Lista de errores si hay campos incompletos.
    """
    required_fields = ["username", "email", "password", "confirm_password"]
    errors = []

    for field in required_fields:
        if not form_data.get(field):
            errors.append(f"El campo '{field}' es obligatorio.")

    # Validar que las contraseñas coincidan
    if "password" in form_data and "confirm_password" in form_data:
        if form_data["password"] != form_data["confirm_password"]:
            errors.append("Las contraseñas no coinciden.")

    return len(errors) == 0, errors

def validate_password_match(password, confirm_password):
    """
    Verifica si las contraseñas ingresadas coinciden.

    Args:
        password (str): La contraseña ingresada.
        confirm_password (str): La confirmación de la contraseña ingresada.

    Returns:
        tuple: (bool, str) -> Un booleano indicando si coinciden y un mensaje de error si no.
    """
    if password != confirm_password:
        return False, "Las contraseñas no coinciden. Por favor, verifica ambas."
    return True, "Las contraseñas coinciden."


# Ejecutar los tests
try:
   
    test_valid_user_registration()
    test_user_name_minimum_two_words()
    test_email_format_and_uniqueness()
    test_password_validity()
    test_form_submission()
    test_password_match()
    
   
finally:
    # Cerrar el navegador
    driver.quit()
