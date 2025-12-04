# A.2 — Navegación y Búsqueda en El Corte Inglés (POM & unittest)

## 1. Objetivo

Automatizar una secuencia de navegación en la web de El Corte Inglés utilizando Python y Selenium. Se debe aplicar rigurosamente el patrón Page Object Model (POM) y verificar cada etapa crítica mediante la librería de pruebas unitarias unittest.

---

## 2. Requisitos clave

* **Tecnologías**: Python, Selenium WebDriver,  unittest.
* **Navegador**: Chrome como navegador recomendado.
* **Estructura**: El código debe estar organizado bajo el patrón POM (separando localizadores y acciones de la lógica de prueba).
* **Independencia**: Todos los tests unitarios deben ser independientes (no deben fallar por el resultado de un test anterior).
* El código fuente debe escribirse en inglés con un correcto nombre para variables y funciones

---

## 3. Consideraciones importantes

La página web de "El Corte ingles" dispone de un mecanismo de protección que rechaza las peticiones al servidor realizadas por un navegador controlado de forma automática. Para evitar esta eventualidad y poder realizar los tests de esta práctica de forma correcta debemos configurar una serie de opciones de manera conveniente durante la creación del la instancia del driver, tal y como se muestra en el siguiente fragmento de código:

```python
options = Options()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
self.service = Service(ChromeDriverManager().install())
self.driver = webdriver.Chrome(service=self.service, options=options)
```

---

## 4. Pasos de la práctica

El alumno debe crear un script de Python que cubra las siguientes secuencias, implementando un test unitario para la verificación de cada fase (un total de cuatro tests independientes, los tres primeros de obligado desarrollo y el último de carácter opcional).

### 4.1: Acceso a la Home y Cookies (Test 1)

* **Acción**: Navegar a la URL principal de El Corte Inglés (https://www.elcorteingles.es/).
* **Acción**: Implementar la lógica para aceptar las cookies que aparecen al inicio.
* **Verificación (unittest)**: Comprobar que la URL actual contiene la cadena "elcorteingles.es".

### 4.2: Búsqueda de un Producto (Test 2)

* **Acción**: desde la página principal, ejecutar una búsqueda por un término predefinido (por ejemplo, `zapatillas`) usando la barra de búsqueda.
* **Verificación (unittest)**: Comprobar que la URL de la página de resultados contiene el término de búsqueda (ej. q=zapatillas, donde q es el nombre del query param).
* **Verificación (unittest)**: Comprobar que el título visible de la página de resultados contiene la palabra "zapatillas"

### 4.3: Acceder al Detalle (Test 3)

* **Acción**: En la página de resultados de la búsqueda anterior hacer clic en el primer producto del listado.
* **Verificación (unittest)**: Comprobar que la URL final es diferente a la URL de la página de resultados (lo que confirma que se ha accedido a la ficha de detalle del producto). Además buscar un elemento del DOM que corrobore que estamos en la página de detalle.

### 4.4: Aplicar Filtro al resultado de la búsqueda inicial (Test 4) - 20% de la nota (Opcional) 

* **Acción**: En la página de resultados de la búsqueda resultante de haber buscado ""zapatillas", aplicar un filtro disponible del menú desplegable: selección de una "marca específica".
* **Verificación (unittest)**: Comprobar que el filtrado ha tenido lugar, por ejemplo mediante la comprobación del número de elementos encontrados.

> Se valorará entregar parcialmente este test (por ejemplo, sólo la acción de abrir el menú y seleccionar la marca), siempre que se documente lo que falta y por qué.

**Autor**: Illian Santiago Ortega Posso

**Asignatura**: PUK
