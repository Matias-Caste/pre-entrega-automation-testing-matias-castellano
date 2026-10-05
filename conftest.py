"""Configuración compartida de Pytest.

Pytest carga este archivo automáticamente. Acá definimos el fixture `driver`,
que abre un Chrome nuevo para cada test y lo cierra al terminar. Así los tests
son independientes: si uno falla, no afecta a los demás.

Nota sobre esperas: NO configuramos espera implícita (implicitly_wait) porque
usamos esperas explícitas (WebDriverWait). Mezclar las dos puede generar
tiempos de espera impredecibles.
"""
import pytest
from selenium import webdriver


@pytest.fixture
def driver():
    opciones = webdriver.ChromeOptions()
    opciones.add_argument("--start-maximized")
    # Desactiva el popup de "guardar contraseña" de Chrome, que puede tapar la página
    opciones.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
        },
    )

    navegador = webdriver.Chrome(options=opciones)
    yield navegador   # acá se ejecuta el test
    navegador.quit()  # esto corre siempre, pase o falle el test
