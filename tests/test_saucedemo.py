"""
tests/test_saucedemo.py
Suite principal de tests para la automatización de SauceDemo.

Cubre:
  - TC01: Login exitoso con credenciales válidas
  - TC02: Login fallido con credenciales inválidas
  - TC03: Título y elementos de la página de inventario
  - TC04: Presencia y detalle del primer producto
  - TC05: Agregar producto al carrito y verificar badge
  - TC06: Verificar ítem dentro del carrito
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.helpers import (
    login,
    is_logged_in,
    get_page_title,
    get_product_names,
    get_product_prices,
    add_first_product_to_cart,
    get_cart_count,
    go_to_cart,
    get_cart_item_names,
    take_screenshot,
    VALID_USER,
    VALID_PASSWORD,
    INVENTORY_URL,
)


# ──────────────────────────────────────────────────────────────────
# BLOQUE 1 – Automatización de Login
# ──────────────────────────────────────────────────────────────────

class TestLogin:
    """Tests relacionados con el flujo de autenticación."""

    def test_login_exitoso(self, driver):
        """
        TC01 – Login con credenciales válidas.
        Verifica redirección a /inventory.html y presencia del título 'Products'.
        """
        login(driver, VALID_USER, VALID_PASSWORD)

        # Espera explícita: URL debe contener /inventory.html
        assert is_logged_in(driver), (
            f"Se esperaba ser redirigido a {INVENTORY_URL}, "
            f"pero la URL actual es: {driver.current_url}"
        )

        # Validación adicional: título de la app en el <title> del documento
        assert "Swag Labs" in driver.title, (
            f"Se esperaba 'Swag Labs' en el título del documento, "
            f"pero se encontró: '{driver.title}'"
        )

    def test_login_fallido_credenciales_incorrectas(self, driver):
        """
        TC02 – Login con credenciales inválidas.
        Verifica que aparezca el mensaje de error y NO se redirija al inventario.
        """
        login(driver, "usuario_invalido", "clave_incorrecta")

        # Debe permanecer en la página de login
        assert "/inventory.html" not in driver.current_url, (
            "No debería haberse redirigido al inventario con credenciales inválidas."
        )

        # Debe mostrar el contenedor de error
        wait = WebDriverWait(driver, 10)
        error_el = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "error-message-container"))
        )
        assert error_el.is_displayed(), "El mensaje de error debería ser visible."


# ──────────────────────────────────────────────────────────────────
# BLOQUE 2 – Navegación y Verificación del Catálogo
# ──────────────────────────────────────────────────────────────────

class TestCatalogo:
    """Tests que validan el catálogo de productos tras el login."""

    def test_titulo_pagina_inventario(self, logged_in_driver):
        """
        TC03 – Título de la página de inventario.
        Verifica que el encabezado visible diga 'Products'.
        """
        titulo = get_page_title(logged_in_driver)

        assert titulo == "Products", (
            f"Se esperaba el título 'Products', pero se encontró: '{titulo}'"
        )

    def test_elementos_interfaz_presentes(self, logged_in_driver):
        """
        TC03b – Elementos de UI presentes en el inventario.
        Valida la presencia del menú hamburguesa y el selector de filtro.
        """
        driver = logged_in_driver

        # Menú lateral (hamburger)
        menu_button = driver.find_element(By.ID, "react-burger-menu-btn")
        assert menu_button.is_displayed(), "El botón de menú debería estar visible."

        # Selector de ordenamiento
        sort_select = driver.find_element(By.CLASS_NAME, "product_sort_container")
        assert sort_select.is_displayed(), "El selector de filtro debería estar visible."

    def test_productos_visibles_en_inventario(self, logged_in_driver):
        """
        TC04 – Presencia de productos en el catálogo.
        Verifica que exista al menos un producto listado.
        """
        nombres = get_product_names(logged_in_driver)

        assert len(nombres) > 0, "Debería haber al menos un producto en el inventario."

    def test_detalle_primer_producto(self, logged_in_driver):
        """
        TC04b – Nombre y precio del primer producto.
        Verifica que el primer producto tenga nombre no vacío y precio con formato '$X.XX'.
        """
        nombres = get_product_names(logged_in_driver)
        precios = get_product_prices(logged_in_driver)

        primer_nombre = nombres[0]
        primer_precio = precios[0]

        assert primer_nombre != "", "El nombre del primer producto no debería estar vacío."
        assert primer_precio.startswith("$"), (
            f"El precio debería comenzar con '$', pero se encontró: '{primer_precio}'"
        )

        print(f"\n  → Primer producto: '{primer_nombre}' | Precio: {primer_precio}")


# ──────────────────────────────────────────────────────────────────
# BLOQUE 3 – Interacción con el Carrito
# ──────────────────────────────────────────────────────────────────

class TestCarrito:
    """Tests que validan el flujo de agregar productos al carrito."""

    def test_agregar_producto_incrementa_badge(self, logged_in_driver):
        """
        TC05 – Agregar primer producto al carrito.
        Verifica que el badge del carrito pase de 0 a 1.
        """
        driver = logged_in_driver

        # Badge debe estar vacío al inicio
        count_inicial = get_cart_count(driver)
        assert count_inicial == 0, (
            f"El carrito debería estar vacío al inicio, pero tiene {count_inicial} ítem/s."
        )

        # Agregar el primer producto
        producto_agregado = add_first_product_to_cart(driver)
        print(f"\n  → Producto agregado: '{producto_agregado}'")

        # Badge debe mostrar 1
        count_posterior = get_cart_count(driver)
        assert count_posterior == 1, (
            f"El badge del carrito debería ser 1, pero muestra: {count_posterior}"
        )

    def test_producto_aparece_en_carrito(self, logged_in_driver):
        """
        TC06 – Verificar ítem en el carrito.
        Agrega el primer producto, navega al carrito y valida que aparezca en la lista.
        """
        driver = logged_in_driver

        # Agregar producto y recordar su nombre
        producto_esperado = add_first_product_to_cart(driver)

        # Navegar al carrito
        go_to_cart(driver)

        # Verificar que la URL sea la del carrito
        assert "/cart.html" in driver.current_url, (
            f"Se esperaba estar en /cart.html, pero la URL es: {driver.current_url}"
        )

        # Verificar que el producto esté en el carrito
        items_en_carrito = get_cart_item_names(driver)
        assert producto_esperado in items_en_carrito, (
            f"Se esperaba encontrar '{producto_esperado}' en el carrito, "
            f"pero los ítems encontrados son: {items_en_carrito}"
        )

        print(f"\n  → Producto '{producto_esperado}' confirmado en el carrito ✓")

    def test_boton_cambia_a_remove_al_agregar(self, logged_in_driver):
        """
        TC05b – El botón 'Add to cart' cambia a 'Remove' tras agregar el producto.
        """
        driver = logged_in_driver
        add_first_product_to_cart(driver)

        # Buscar el botón que ahora debería decir "Remove"
        remove_button = driver.find_element(
            By.CSS_SELECTOR, ".inventory_item button.btn_secondary"
        )
        assert "Remove" in remove_button.text, (
            f"Se esperaba el texto 'Remove' en el botón, "
            f"pero dice: '{remove_button.text}'"
        )


# ──────────────────────────────────────────────────────────────────
# Hook para captura automática ante fallos
# ──────────────────────────────────────────────────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook de Pytest: captura automáticamente una screenshot cuando un test falla.
    La imagen se guarda en la carpeta reports/ con el nombre del test.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver") or item.funcargs.get("logged_in_driver")
        if driver:
            test_name = item.name.replace(" ", "_")
            path = take_screenshot(driver, f"FALLO_{test_name}")
            print(f"\n  📸 Screenshot guardada en: {path}")
