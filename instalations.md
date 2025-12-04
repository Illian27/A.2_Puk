Lo primero de todo es instalar python.

# Windows
Con windows puedes ejecutar el archivo de requisitos una vez instalado también "pip" con el siguiente comando: pip install -r requirements.txt

---

# Linux
La forma más comoda es:
* Crear un entorno virtual en la raíz del proyecto: python -m venv .venv
* Activarlo (si no usas fish como shell quita la extensión ".fish"): source .venv/bin/activate.fish 
* Instalar las dependencias: pip install -r requirements.txt
---

Para ejecutar los test: python -m unittest tests/test.py -v