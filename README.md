# Pruebas Técnicas Induze

Este proyecto contiene pruebas automatizadas desarrolladas en Python utilizando Selenium para realizar pruebas de funcionalidad en una plataforma web.

```plaintext
├── env/
├── pages/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── base_page.py
│   ├── login_page.py
│   ├── register_page.py
├── tests/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── test_login.py
│   ├── test_register.py
├── chromedriver.exe
├── config.py
├── requirements.txt
├── .gitignore
```

## Pre-requisitos

- Python 3.9 o superior.
- Google Chrome (versión 132.0.6834.84 o superior).
- [Chromedriver](https://sites.google.com/chromium.org/driver/) (debe coincidir con la versión de tu navegador).

## Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone <url-del-repositorio>
   cd pruebas-tecnicas-induze
   ```

2. **Crear y activar un entorno virtual**:
   ```bash
   python -m venv env
   source env/bin/activate   # En Windows: env\Scripts\activate
   ```

3. **Instalar las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar las variables globales en `config.py`**:
   Edita el archivo `config.py` y asegúrate de establecer los valores correctos para:
   ```python
   CHROME_DRIVER_PATH = "chromedriver.exe"
   EMAIL = "oscarguerr0205@gmail.com"
   PASSWORD = "Oscarguerr12."
   EMAIL_INVALID = "oscarguerr02a05@gmail.com"
   PASSWORD_INVALID = "Oscarguerr12."
   ```
   **Nota:** Estas variables globales están destinadas exclusivamente para la ejecución de las pruebas de login y no deben ser utilizadas en otros contextos.

## Ejecución de pruebas

1. **Pruebas de login**:
   ```bash
   python -m tests.test_login
   ```

2. **Pruebas de registro**:
   ```bash
   python -m tests.test_register
   ```

## Descripción de pruebas

- `test_login_successful()`: Verifica que el usuario puede iniciar sesión con credenciales válidas.
- `test_login_form_empty_fields()`: Valida que el formulario de login no se envíe si los campos están incompletos.
- `test_user_name_displayed_after_login()`: Comprueba que el nombre del usuario se muestre correctamente tras iniciar sesión.
- `test_logout_functionality()`: Verifica que el usuario puede cerrar sesión correctamente.

- `test_register_successful()`: Valida que el registro de un usuario con datos válidos se complete correctamente.
- `test_register_invalid_email()`: Comprueba que el sistema muestra un error al intentar registrar un usuario con un correo no válido.
- `test_register_empty_fields()`: Verifica que no se permita registrar usuarios si los campos obligatorios están vacíos.
- `test_register_existing_email()`: Valida que el sistema rechace intentos de registro con un correo electrónico ya registrado.

## Notas adicionales

- Asegúrate de que el archivo `chromedriver.exe` esté en la raíz del proyecto y sea compatible con la versión de Google Chrome instalada en tu sistema.
- Si encuentras problemas, verifica que las dependencias estén correctamente instaladas y que las rutas en `config.py` sean válidas.

## Contacto

Para dudas, contacta con [oscarguerr0205@gmail.com](mailto:oscarguerr0205@gmail.com).

