# Plan de Desarrollo — Tienda de Música (Flask + PostgreSQL)

## Descripción general del proyecto

Aplicación web de gestión de inventario para una tienda de artículos musicales (vinilos, CDs, merch, amplificadores, cables, speakers, receivers, etc.). Cada usuario registrado administra únicamente los productos/registros que él mismo crea.

**Stack tecnológico:**

| Componente | Tecnología |
|---|---|
| Lenguaje | Python 3.11+ |
| Framework web | Flask |
| Base de datos | PostgreSQL |
| ORM | SQLAlchemy (Flask-SQLAlchemy) |
| Migraciones | Flask-Migrate (Alembic) |
| Autenticación | Flask-Login + Werkzeug (hash de contraseñas) |
| Formularios | Flask-WTF (opcional, recomendado) |
| Frontend | HTML + CSS + Jinja2 |
| Control de versiones | Git |
| Repositorio | GitHub |
| Despliegue | Render (PaaS) |
| Servidor WSGI producción | Gunicorn |

---

## Paso 1 — Diseño y arquitectura

**Objetivo:** definir la estructura del proyecto y el modelo de datos antes de escribir código.

### 1.1 Modelo de datos

Dos tablas mínimas, con relación uno a muchos (Usuario → Productos):

**Tabla `usuarios`**
- `id` (PK, integer)
- `nombre_usuario` (string, único)
- `email` (string, único)
- `password_hash` (string)
- `fecha_registro` (datetime)

**Tabla `productos`**
- `id` (PK, integer)
- `nombre` (string)
- `categoria` (string) — vinilo, cd, merch, amplificador, cable, speaker, receiver, etc.
- `descripcion` (text)
- `precio` (numeric)
- `stock` (integer)
- `fecha_creacion` (datetime)
- `usuario_id` (FK → usuarios.id)

Relación: `usuario.productos` (uno a muchos). Cada consulta de productos se filtra siempre por `usuario_id` del usuario en sesión.

### 1.2 Estructura de carpetas propuesta

```
tienda-musica/
├── app/
│   ├── __init__.py        (application factory, inicializa db, login manager)
│   ├── models.py          (Usuario, Producto)
│   ├── routes/
│   │   ├── auth.py        (registro, login, logout)
│   │   └── productos.py   (CRUD)
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   └── productos/
│   └── static/
│       └── css/
├── config.py               (configuración, variables de entorno)
├── requirements.txt
├── run.py                  (punto de entrada)
├── .env                    (variables locales, no se sube a Git)
├── .gitignore
└── README.md
```

### 1.3 Diseño de rutas (endpoints)

| Ruta | Método | Función |
|---|---|---|
| `/registro` | GET/POST | Crear usuario |
| `/login` | GET/POST | Iniciar sesión |
| `/logout` | GET | Cerrar sesión |
| `/productos` | GET | Listar productos del usuario |
| `/productos/nuevo` | GET/POST | Crear producto |
| `/productos/<id>/editar` | GET/POST | Modificar producto |
| `/productos/<id>/eliminar` | POST | Eliminar producto |

**Entregable de este paso:** este documento + diagrama simple de tablas (puede hacerse en papel o herramienta de diagramación).

---

## Paso 2 — Configuración del entorno y base de datos

**Objetivo:** dejar el entorno de desarrollo funcional con PostgreSQL conectado a Flask.

1. Crear repositorio en GitHub e inicializar Git localmente (`git init`, primer commit).
2. Crear entorno virtual: `python -m venv venv`.
3. Instalar dependencias base: `Flask`, `Flask-SQLAlchemy`, `Flask-Migrate`, `Flask-Login`, `psycopg2-binary`, `python-dotenv`, `gunicorn`.
4. Instalar PostgreSQL localmente y crear base de datos de desarrollo (ej. `tienda_musica_dev`).
5. Configurar `config.py` para leer `DATABASE_URL` desde variables de entorno (usar `.env` local, nunca hardcodear credenciales).
6. Definir modelos en `models.py` (Usuario, Producto) con Flask-SQLAlchemy.
7. Inicializar Flask-Migrate y generar la primera migración (`flask db init`, `flask db migrate`, `flask db upgrade`) para crear las tablas en PostgreSQL.
8. Verificar con un cliente (psql, DBeaver o pgAdmin) que las tablas se crearon correctamente.

**Entregable de este paso:** proyecto en Git con conexión funcional a PostgreSQL y tablas creadas mediante migraciones.

---

## Paso 3 — Desarrollo de funcionalidades

**Objetivo:** implementar la lógica de autenticación y el CRUD completo.

### 3.1 Gestión de usuarios
- Registro: formulario que valida usuario/email único, guarda contraseña con hash (`werkzeug.security.generate_password_hash`).
- Login: valida credenciales, usa Flask-Login (`login_user`) para crear la sesión.
- Logout: `logout_user()`.
- Protección de rutas: decorador `@login_required` en todas las rutas de productos.

### 3.2 CRUD de productos
- Create: formulario para agregar producto, asociado automáticamente a `current_user.id`.
- Read: listado que consulta solo `Producto.query.filter_by(usuario_id=current_user.id)`.
- Update: formulario de edición, con verificación de que el producto pertenezca al usuario en sesión (evitar que un usuario edite registros ajenos manipulando la URL).
- Delete: eliminación con la misma verificación de propiedad.

### 3.3 Frontend
- Plantilla base (`base.html`) con navegación (login/logout, enlace a productos).
- Vistas simples en HTML + CSS: formularios de registro/login, tabla o tarjetas de productos, formularios de creación/edición.
- Mensajes flash para confirmar acciones (creado, actualizado, eliminado, error de credenciales).

**Entregable de este paso:** aplicación funcionando localmente cumpliendo los 8 requisitos mínimos funcionales (registro, login, logout, crear, leer, actualizar, eliminar, aislamiento de datos por usuario).

---

## Paso 4 — Pruebas, control de versiones y despliegue en Render

**Objetivo:** validar la app localmente, subirla a GitHub y desplegarla en Render.

### 4.1 Pruebas locales (checklist antes de desplegar)
- Registrar dos usuarios distintos y verificar que cada uno solo ve sus propios productos.
- Probar crear, editar y eliminar productos.
- Verificar que cerrar la app y volver a abrirla mantiene los datos (persistencia en PostgreSQL).
- Probar accesos no autorizados (intentar editar/eliminar un producto ajeno vía URL directa).

### 4.2 Control de versiones
- Commits organizados por funcionalidad (estructura inicial, modelos, auth, CRUD, frontend, despliegue).
- Archivo `.gitignore` que excluya `venv/`, `.env`, `__pycache__/`.
- Repositorio subido a GitHub con `README.md` explicando cómo ejecutar el proyecto localmente.

### 4.3 Preparación para despliegue
- Agregar `requirements.txt` actualizado (`pip freeze > requirements.txt`).
- Crear archivo `Procfile` o configurar el "Start Command" en Render: `gunicorn run:app`.
- Asegurar que la app lea `DATABASE_URL` desde variable de entorno (Render la provee automáticamente si se crea la base de datos ahí).

### 4.4 Despliegue en Render
1. Crear una base de datos PostgreSQL en Render (plan gratuito/PaaS).
2. Crear un "Web Service" en Render conectado al repositorio de GitHub.
3. Configurar variables de entorno en Render (`DATABASE_URL`, `SECRET_KEY`).
4. Configurar comando de build (`pip install -r requirements.txt`) y comando de inicio (`gunicorn run:app`).
5. Ejecutar migraciones en producción (`flask db upgrade`) desde la consola de Render o como parte del build.
6. Verificar que la app despliega correctamente y que los datos persisten entre reinicios del servicio.

**Entregable final:** aplicación desplegada en Render, accesible públicamente, con código en GitHub y base de datos PostgreSQL persistente.

---

## Resumen de cumplimiento de requisitos

- [x] Registro, login, logout — Paso 3
- [x] Control de acceso y aislamiento de datos por usuario — Paso 3
- [x] CRUD completo — Paso 3
- [x] PostgreSQL + SQLAlchemy — Paso 2
- [x] Persistencia de datos — Paso 2 y 4
- [x] Git + GitHub — Paso 2 y 4
- [x] Despliegue en Render (PaaS) — Paso 4
