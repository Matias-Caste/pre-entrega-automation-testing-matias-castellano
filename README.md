# Pre-entrega Automation Testing – saucedemo.com

## Propósito
Automatizar con Selenium y Pytest tres flujos básicos de https://www.saucedemo.com: login y verificación del catálogo de productos y agregado de un producto al carrito.

## Tecnologías utilizadas
- Python 3
- Selenium WebDriver (Chrome)
- Pytest y pytest-html (reporte)
- Git y GitHub

## Estructura del proyecto

tests/test_saucedemo.py   -> casos de prueba
utils/helpers.py          -> funciones auxiliares (login, esperas, capturas, log)
conftest.py               -> fixture que abre y cierra el navegador
reports/                  -> reporte HTML, log y capturas de pantalla
requirements.txt          -> dependencias


## Casos de prueba
1. **test_login_exitoso**: inicia sesión con `standard_user` y valida la redirección a `/inventory.html` y los textos "Products" y "Swag Labs".
2. **test_catalogo_navegacion**: valida el título de la página, que haya productos, que existan el menú, el filtro y el carrito, e imprime nombre y precio del primer producto.
3. **test_agregar_producto_al_carrito**: agrega el primer producto, valida que el contador sea 1, entra al carrito y verifica que el producto (nombre y precio) sea el correcto.

Cada test abre su propio navegador, por lo que son independientes entre sí.

## Conceptos aplicados
- **Localizadores**: ID, NAME, CSS Selector, XPath y Class Name.
- **Interacciones**: `click()`, `send_keys()`, `clear()`, `.text` y `get_attribute()`.
- **Formulario de login**: se completan usuario y contraseña y se verifica con `get_attribute("value")` lo escrito.
- **Esperas explícitas**: `WebDriverWait` con `visibility_of_element_located` y `url_contains`. No se usa espera implícita para evitar mezclar ambos tipos de espera.

## Instalación de dependencias
Requiere tener Python y Google Chrome instalados.

python -m venv venv
venv\Scripts\activate        
pip install -r requirements.txt

## Ejecución de las pruebas
pytest tests/test_saucedemo.py -v --html=reports/reporte.html --self-contained-html


## Evidencias
- `reports/reporte.html`: reporte de resultados de la ejecución.
- `reports/ejecucion.log`: log de la ejecución.
- `reports/screenshots/`: capturas de pantalla automáticas cuando un test falla.
