"""Funciones auxiliares para los tests de saucedemo.com."""
import logging
import os
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# ---------- Datos de prueba ----------
URL = "https://www.saucedemo.com/"
USUARIO = "standard_user"
PASSWORD = "secret_sauce"
TIEMPO_ESPERA = 10  # segundos máximos para las esperas explícitas

# ---------- Carpetas de reportes y log ----------
CARPETA_REPORTS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
CARPETA_CAPTURAS = os.path.join(CARPETA_REPORTS, "screenshots")
os.makedirs(CARPETA_CAPTURAS, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(CARPETA_REPORTS, "ejecucion.log"),
    level=logging.INFO,
    encoding="utf-8",
    force=True,  # pytest ya configura el logging; force=True hace que se cree igual el archivo
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def esperar_elemento(driver, by, valor):
    """Espera EXPLÍCITA: hasta TIEMPO_ESPERA segundos a que el elemento sea visible.

    A diferencia de una espera implícita (que aplica a todos los find_element),
    esta espera una condición concreta sobre un elemento concreto.
    """
    return WebDriverWait(driver, TIEMPO_ESPERA).until(
        EC.visibility_of_element_located((by, valor))
    )


def login(driver, usuario, password):
    """Completa el formulario de login de saucedemo.com y hace clic en 'Login'."""
    logging.info("Iniciando sesión con el usuario '%s'", usuario)
    driver.get(URL)

    # Localizamos los campos por ID y por NAME
    campo_usuario = esperar_elemento(driver, By.ID, "user-name")
    campo_password = driver.find_element(By.NAME, "password")

    # clear() deja el campo vacío antes de escribir; send_keys() escribe el texto
    campo_usuario.clear()
    campo_usuario.send_keys(usuario)
    campo_password.clear()
    campo_password.send_keys(password)

    # get_attribute("value") devuelve lo que realmente hay escrito en el input
    assert campo_usuario.get_attribute("value") == usuario, "El usuario no se escribió bien"

    driver.find_element(By.ID, "login-button").click()


def obtener_primer_producto(driver):
    """Devuelve el nombre y el precio del primer producto del catálogo (con XPath)."""
    # (...)[1] toma el primer resultado. contains(@class, ...) evita depender
    # del valor exacto del atributo class.
    nombre = esperar_elemento(
        driver, By.XPATH, "(//div[contains(@class,'inventory_item_name')])[1]"
    ).text
    precio = driver.find_element(
        By.XPATH, "(//div[contains(@class,'inventory_item_price')])[1]"
    ).text
    logging.info("Primer producto: %s - %s", nombre, precio)
    return nombre, precio


def guardar_captura(driver, nombre_test):
    """Guarda una captura de pantalla en reports/screenshots (se usa cuando un test falla)."""
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta = os.path.join(CARPETA_CAPTURAS, f"{nombre_test}_{fecha}.png")
    driver.save_screenshot(ruta)
    logging.error("Test fallido. Captura guardada en %s", ruta)