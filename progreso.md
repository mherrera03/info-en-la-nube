# Tienda de Música

Aplicación web de gestión de inventario (vinilos, CDs, merch, amplificadores, cables, speakers, receivers) desarrollada con Flask, PostgreSQL y SQLAlchemy.

## Estado actual (Paso 3 del plan completado)

- Estructura del proyecto, modelos y migraciones (Paso 1 y 2).
- Autenticación: registro, login, logout con Flask-Login (`app/routes/auth.py`).
- CRUD de productos completo, aislado por usuario (`app/routes/productos.py`).
- Formularios con validación server-side vía Flask-WTF (`app/forms.py`), incluye protección CSRF en toda la app (`CSRFProtect`).
- Plantillas Jinja2: `base.html` con navegación y mensajes flash, vistas de login/registro y listado/formulario de productos.
- Verificado con una suite de pruebas end-to-end contra PostgreSQL real: registro, duplicados rechazados, login, CSRF (rechaza POST sin token), crear/editar/eliminar producto, aislamiento entre usuarios (403 al intentar tocar productos ajenos), y redirección a login en rutas protegidas sin sesión.

Aún falta (próximo paso): checklist de pruebas manuales, preparación y despliegue en Render (Paso 4).

## Instalación local

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # y edita los valores
```

Base de datos y migraciones:

```bash
createdb tienda_musica_dev
flask db upgrade
```

Ejecuta la app:

```bash
python run.py
```

Rutas disponibles: `/registro`, `/login`, `/logout`, `/productos`, `/productos/nuevo`, `/productos/<id>/editar`, `/productos/<id>/eliminar`.
