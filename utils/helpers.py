"""
utils/helpers.py
Funciones auxiliares reutilizables para los tests de automatización de SauceDemo.
"""

import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException


# ──────────────────────────────────────────────
# Constantes del sitio
# ──────────────────────────────────────────────
BASE_URL = "https://www.saucedemo.com"
INVENTORY_URL = f"{BASE_URL}/inventory.html"

VALID_USER = "standard_user"
VALID_PASSWORD = "secret_sauce"

DEFAULT_TIMEOUT = 10  # segundos para esperas explícitas


# ──────────────────────────────────────────────
# Configuración del driver
# ──────────────────────────────────────────────
def get_driver(headless: bool = True) -> webdriver.Chrome:
    """
    Crea y retorna una instancia de Chrome WebDriver.

    Args:
        headless: Si True, ejecuta el navegador en modo sin interfaz gráfica.

    Returns:
        Instancia de webdriver.Chrome configurada.
    """
    options = Options()

    if headless:
        options.add_argument("--headless=new")

    # Opciones recomendadas para entornos CI / Docker
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(3)
    return driver


# ──────────────────────────────────────────────
# Acciones de login
# ──────────────────────────────────────────────
def login(driver: webdriver.Chrome, username: str, password: str) -> None:
    """
    Navega a la página de login e ingresa las credenciales indicadas.

    Args:
        driver: Instancia activa del WebDriver.
        username: Nombre de usuario.
        password: Contraseña.
    """
    driver.get(BASE_URL)

    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    # Esperar a que el campo usuario esté disponible
    user_input = wait.until(
        EC.presence_of_element_located((By.ID, "user-name"))
    )
    user_input.clear()
    user_input.send_keys(username)

    password_input = driver.find_element(By.ID, "password")
    password_input.clear()
    password_input.send_keys(password)

    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()


def is_logged_in(driver: webdriver.Chrome) -> bool:
    """
    Verifica si el driver está en la página de inventario (login exitoso).

    Returns:
        True si la URL actual corresponde al inventario.
    """
    try:
        WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.url_contains("/inventory.html")
        )
        return True
    except TimeoutException:
        return False


# ──────────────────────────────────────────────
# Acciones sobre el catálogo
# ──────────────────────────────────────────────
def get_product_names(driver: webdriver.Chrome) -> list[str]:
    """
    Retorna la lista de nombres de todos los productos visibles en el inventario.

    Returns:
        Lista de strings con los nombres de los productos.
    """
    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)
    items = wait.until(
        EC.presence_of_all_elements_located(
            (By.CLASS_NAME, "inventory_item_name")
        )
    )
    return [item.text for item in items]


def get_product_prices(driver: webdriver.Chrome) -> list[str]:
    """
    Retorna la lista de precios de todos los productos visibles en el inventario.

    Returns:
        Lista de strings con los precios (ej. "$9.99").
    """
    items = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
    return [item.text for item in items]


def get_page_title(driver: webdriver.Chrome) -> str:
    """
    Retorna el título visible del encabezado de la página de inventario.

    Returns:
        Texto del elemento .title (ej. "Products").
    """
    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)
    title_el = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "title"))
    )
    return title_el.text


# ──────────────────────────────────────────────
# Acciones sobre el carrito
# ──────────────────────────────────────────────
def add_first_product_to_cart(driver: webdriver.Chrome) -> str:
    """
    Agrega el primer producto disponible al carrito.

    Returns:
        Nombre del producto agregado.
    """
    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    # Obtener nombre del primer producto antes de agregar
    product_name = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_item_name"))
    ).text

    # Hacer clic en el botón "Add to cart" del primer producto
    add_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".inventory_item button")
        )
    )
    add_button.click()

    return product_name


def get_cart_count(driver: webdriver.Chrome) -> int:
    """
    Retorna el número de ítems indicado en el badge del carrito.

    Returns:
        Cantidad de ítems como entero; 0 si el badge no está presente.
    """
    try:
        badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        return int(badge.text)
    except NoSuchElementException:
        return 0


def go_to_cart(driver: webdriver.Chrome) -> None:
    """Navega al carrito de compras haciendo clic en el ícono."""
    cart_icon = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    cart_icon.click()

    WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.url_contains("/cart.html")
    )


def get_cart_item_names(driver: webdriver.Chrome) -> list[str]:
    """
    Retorna los nombres de los productos dentro del carrito.

    Returns:
        Lista de strings con los nombres de los ítems en el carrito.
    """
    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)
    items = wait.until(
        EC.presence_of_all_elements_located(
            (By.CLASS_NAME, "inventory_item_name")
        )
    )
    return [item.text for item in items]


# ──────────────────────────────────────────────
# Capturas de pantalla
# ──────────────────────────────────────────────
def take_screenshot(driver: webdriver.Chrome, name: str) -> str:
    """
    Guarda una captura de pantalla en la carpeta reports/.

    Args:
        driver: Instancia activa del WebDriver.
        name: Nombre descriptivo del archivo (sin extensión).

    Returns:
        Ruta relativa del archivo guardado.
    """
    reports_dir = os.path.join(os.path.dirname(__file__), "..", "reports")
    os.makedirs(reports_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.png"
    filepath = os.path.join(reports_dir, filename)

    driver.save_screenshot(filepath)
    return filepath
