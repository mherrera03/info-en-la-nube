# Tienda de Música

Aplicación web de gestión de inventario (vinilos, CDs, merch, amplificadores, cables, speakers, receivers) desarrollada con Flask, PostgreSQL y SQLAlchemy.

## Estado actual (Paso 1 del plan)

- Estructura del proyecto creada.
- Modelos definidos: `Usuario` y `Producto` (relación uno a muchos).
- Configuración de base de datos por variables de entorno.

Aún faltan (próximos pasos): migraciones aplicadas, rutas de autenticación, rutas CRUD y plantillas HTML.

## Instalación local

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # y edita los valores
```

Crea la base de datos en PostgreSQL local:

```bash
createdb tienda_musica_dev
```

Inicializa migraciones (se hará en el Paso 2):

```bash
flask db init
flask db migrate -m "tablas iniciales"
flask db upgrade
```

Ejecuta la app:

```bash
python run.py
```
