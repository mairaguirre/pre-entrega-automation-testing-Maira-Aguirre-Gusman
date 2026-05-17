# pre-entrega-automation-testing

Proyecto de automatización de pruebas sobre [SauceDemo](https://www.saucedemo.com), desarrollado como pre-entrega del curso de Testing Automatizado con Selenium y Python.

---

## Propósito

Automatizar y validar los flujos principales de la aplicación SauceDemo:

1. **Login** – credenciales válidas e inválidas.
2. **Catálogo** – título, elementos de UI y detalle del primer producto.
3. **Carrito** – agregar producto, verificar badge y confirmar ítem en el carrito.

---

## Tecnologías utilizadas

| Tecnología | Rol |
|---|---|
| Python 3.11+ | Lenguaje principal |
| Selenium WebDriver 4 | Automatización del navegador |
| Pytest 8 | Framework de testing |
| pytest-html | Generación de reportes HTML |
| webdriver-manager | Gestión automática del ChromeDriver |
| Git / GitHub | Control de versiones |

---

## Estructura del proyecto

```
pre-entrega-automation-testing/
│
├── tests/
│   └── test_saucedemo.py     # Suite principal de tests (TC01 – TC06)
│
├── utils/
│   └── helpers.py            # Funciones auxiliares reutilizables
│
├── reports/                  # Reportes HTML y screenshots de fallos (gitignored)
├── datos/                    # Datos externos (CSV/JSON, si aplica)
│
├── conftest.py               # Fixtures compartidas (driver, logged_in_driver)
├── pytest.ini                # Configuración de Pytest
├── requirements.txt          # Dependencias del proyecto
├── .gitignore
└── README.md
```

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/<tu-usuario>/pre-entrega-automation-testing-<nombre-apellido>.git
cd pre-entrega-automation-testing-<nombre-apellido>
```

### 2. Crear y activar entorno virtual

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

> El paquete `webdriver-manager` descarga automáticamente la versión correcta de ChromeDriver. No es necesario instalarlo manualmente.

---

## Ejecución de las pruebas

### Ejecutar todos los tests con reporte HTML

```bash
pytest tests/test_saucedemo.py -v --html=reports/reporte.html --self-contained-html
```

### Ejecutar un test específico

```bash
pytest tests/test_saucedemo.py::TestLogin::test_login_exitoso -v
```

### Ejecutar sin modo headless (ver el navegador)

Editar `utils/helpers.py` y cambiar la llamada a `get_driver(headless=False)` en `conftest.py`, o agregar una variable de entorno:

```bash
HEADLESS=false pytest tests/test_saucedemo.py -v
```

---

## Casos de prueba

| ID | Clase | Descripción |
|---|---|---|
| TC01 | TestLogin | Login exitoso → redirige a `/inventory.html` |
| TC02 | TestLogin | Login fallido → muestra mensaje de error |
| TC03 | TestCatalogo | Título de la página es "Products" |
| TC03b | TestCatalogo | Menú y filtro de ordenamiento visibles |
| TC04 | TestCatalogo | Al menos un producto presente en el catálogo |
| TC04b | TestCatalogo | Nombre y precio del primer producto con formato correcto |
| TC05 | TestCarrito | Badge del carrito pasa de 0 a 1 al agregar producto |
| TC05b | TestCarrito | Botón cambia de "Add to cart" a "Remove" |
| TC06 | TestCarrito | Producto aparece correctamente dentro del carrito |

---

## Evidencias de fallo

Ante cualquier test fallido, se genera automáticamente una captura de pantalla en la carpeta `reports/` con el prefijo `FALLO_`.

---

## Credenciales de prueba

Las credenciales están definidas como constantes en `utils/helpers.py`:

```python
VALID_USER = "standard_user"
VALID_PASSWORD = "secret_sauce"
```

> SauceDemo es una aplicación pública de práctica. No contiene datos reales.
