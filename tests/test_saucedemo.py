"""Pre-entrega: automatización de saucedemo.com con Selenium y Pytest.

Tests incluidos:
    1. test_login_exitoso
    2. test_catalogo_navegacion
    3. test_agregar_producto_al_carrito

Cada test usa el fixture `driver` (ver conftest.py), por lo que son independientes.
Si un test falla, se guarda una captura de pantalla y se vuelve a lanzar el error
para que Pytest lo marque como fallido.

Estrategias de localización usadas: ID, NAME, CSS_SELECTOR, XPATH y CLASS_NAME.
"""
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.helpers import (
    PASSWORD,
    TIEMPO_ESPERA,
    USUARIO,
    esperar_elemento,
    guardar_captura,
    login,
    obtener_primer_producto,
)


def test_login_exitoso(driver):
    """Login con credenciales válidas: redirige a /inventory.html y muestra 'Products'."""
    try:
        login(driver, USUARIO, PASSWORD)

        # Espera explícita a que la URL cambie a la página de inventario
        WebDriverWait(driver, TIEMPO_ESPERA).until(EC.url_contains("/inventory.html"))
        assert "/inventory.html" in driver.current_url

        # Validamos los textos visibles de la página (CSS con selector de clase)
        titulo_seccion = esperar_elemento(driver, By.CSS_SELECTOR, ".title")
        assert titulo_seccion.text == "Products"
        logo = esperar_elemento(driver, By.CSS_SELECTOR, ".app_logo")
        assert logo.text == "Swag Labs"
        logging.info("Login exitoso verificado")
    except Exception:
        guardar_captura(driver, "test_login_exitoso")
        raise


def test_catalogo_navegacion(driver):
    """Verifica el título, que haya productos y que estén los elementos principales."""
    try:
        login(driver, USUARIO, PASSWORD)
        WebDriverWait(driver, TIEMPO_ESPERA).until(EC.url_contains("/inventory.html"))

        # 1. Título de la pestaña del navegador
        assert driver.title == "Swag Labs"

        # 2. Hay al menos un producto visible
        productos = driver.find_elements(By.CLASS_NAME, "inventory_item")
        assert len(productos) > 0, "No se encontraron productos en el catálogo"
        assert productos[0].is_displayed()

        # 3. Elementos importantes de la interfaz: menú (ID), filtro (CSS) y carrito (XPath)
        assert esperar_elemento(driver, By.ID, "react-burger-menu-btn").is_displayed()
        assert esperar_elemento(driver, By.CSS_SELECTOR, "select.product_sort_container").is_displayed()
        assert esperar_elemento(driver, By.XPATH, "//a[@class='shopping_cart_link']").is_displayed()

        # 4. Nombre y precio del primer producto
        nombre, precio = obtener_primer_producto(driver)
        assert nombre != "", "El primer producto no tiene nombre"
        assert precio.startswith("$"), f"Precio con formato inesperado: {precio}"
        print(f"Primer producto: {nombre} - {precio}")
    except Exception:
        guardar_captura(driver, "test_catalogo_navegacion")
        raise


def test_agregar_producto_al_carrito(driver):
    """Agrega el primer producto, valida el contador y comprueba que esté en el carrito."""
    try:
        login(driver, USUARIO, PASSWORD)
        WebDriverWait(driver, TIEMPO_ESPERA).until(EC.url_contains("/inventory.html"))

        # Guardamos nombre y precio para compararlos después en el carrito
        nombre, precio = obtener_primer_producto(driver)

        # Clic en el botón "Add to cart" del primer producto
        boton_agregar = esperar_elemento(driver, By.CSS_SELECTOR, "button.btn_inventory")
        assert boton_agregar.text == "Add to cart"
        boton_agregar.click()

        # Al hacer clic, la página vuelve a dibujar el botón y la referencia anterior
        # queda obsoleta (StaleElementReferenceException). Por eso esperamos a que el
        # botón diga "Remove" y lo volvemos a buscar en lugar de reutilizar el anterior.
        WebDriverWait(driver, TIEMPO_ESPERA).until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, "button.btn_inventory"), "Remove"
            )
        )
        boton_remove = driver.find_element(By.CSS_SELECTOR, "button.btn_inventory")
        assert boton_remove.text == "Remove"
        # get_attribute("id"): el id pasa de add-to-cart-... a remove-...
        assert "remove" in boton_remove.get_attribute("id")

        # El contador del carrito debe mostrar 1
        contador = esperar_elemento(driver, By.CLASS_NAME, "shopping_cart_badge")
        assert contador.text == "1", f"Contador esperado: 1, obtenido: {contador.text}"

        # Ir al carrito
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        WebDriverWait(driver, TIEMPO_ESPERA).until(EC.url_contains("/cart.html"))

        # find_elements NO espera: devuelve lo que haya en ese instante. Como la URL cambia
        # antes de que el carrito termine de dibujarse, primero esperamos (explícitamente)
        # a que aparezca el primer producto y recién después los listamos.
        esperar_elemento(driver, By.CLASS_NAME, "cart_item")

        # El producto del carrito debe ser el mismo que agregamos
        items = driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(items) == 1, f"Se esperaba 1 producto en el carrito, hay {len(items)}"
        nombre_en_carrito = items[0].find_element(By.XPATH, ".//div[contains(@class,'inventory_item_name')]").text
        precio_en_carrito = items[0].find_element(By.XPATH, ".//div[contains(@class,'inventory_item_price')]").text
        assert nombre_en_carrito == nombre
        assert precio_en_carrito == precio
        logging.info("Producto '%s' verificado en el carrito", nombre)
    except Exception:
        guardar_captura(driver, "test_agregar_producto_al_carrito")
        raise