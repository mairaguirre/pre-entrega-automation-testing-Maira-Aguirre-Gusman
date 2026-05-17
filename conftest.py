"""
conftest.py
Fixtures compartidas por todos los tests.
Pytest las carga automáticamente sin necesidad de importarlas.
"""

import pytest
from utils.helpers import get_driver, login, VALID_USER, VALID_PASSWORD


@pytest.fixture(scope="function")
def driver():
    """
    Fixture que provee un driver Chrome limpio para cada test.
    Abre el navegador antes del test y lo cierra al finalizar (teardown).
    """
    d = get_driver(headless=True)
    yield d
    d.quit()


@pytest.fixture(scope="function")
def logged_in_driver(driver):
    """
    Fixture que provee un driver ya autenticado en SauceDemo.
    Depende de la fixture 'driver' para reutilizar su ciclo de vida.
    """
    login(driver, VALID_USER, VALID_PASSWORD)
    yield driver
