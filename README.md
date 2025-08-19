# Blog API

API REST desarrollada con FastAPI, PostgreSQL y SQLAlchemy siguiendo arquitectura por capas.

Este proyecto **Blog API** es de ejemplo, con autenticación y autorización básica, que permitirá gestionar usuarios y publicaciones.
La API contará con dos tablas principales:

* **Usuarios**: Maneja datos de autenticación, roles, estado de cuenta y metadatos.
* **Publicaciones (Posts)**: Contiene las entradas de blog creadas por los usuarios.

Se implementará seguridad con **OAuth2 + JWT** y se encriptarán las contraseñas, además de validaciones de datos.

---

## 📂 Tablas y campos

### 1️⃣ Tabla `users`

**Propósito:** almacenar la información de cada usuario, incluyendo credenciales, rol y estado.

| Campo          | Tipo SQL     | Restricciones / Validaciones        |
| -------------- | ------------ | ----------------------------------- |
| id             | SERIAL       | PK, autoincremental                 |
| username       | VARCHAR(50)  | Único, requerido, min 3, max 50     |
| email          | VARCHAR(255) | Único, requerido, formato email     |
| password\_hash | TEXT         | Requerido, contraseña encriptada    |
| full\_name     | VARCHAR(100) | Opcional                            |
| role           | VARCHAR(20)  | Valores permitidos: 'admin', 'user' |
| is\_active     | BOOLEAN      | Por defecto `TRUE`                  |
| birth\_date    | DATE         | Opcional, solo fecha de nacimiento  |
| rating         | FLOAT        | Opcional, rango 0.0 - 5.0           |
| created\_at    | TIMESTAMP    | Por defecto `NOW()`                 |
| updated\_at    | TIMESTAMP    | Actualiza en cada cambio            |

**Notas:**

* La contraseña nunca se almacena en texto plano.
* El rol determina permisos sobre la API.
* `is_active` permite deshabilitar una cuenta sin eliminarla.
* `birth_date` usa solo fecha sin hora.

---

### 2️⃣ Tabla `posts`

**Propósito:** almacenar las entradas del blog asociadas a usuarios.

| Campo         | Tipo SQL         | Restricciones / Validaciones         |
| ------------- | ---------------- | ------------------------------------ |
| id            | UUID             | PK, generado con `gen_random_uuid()` |
| user\_id      | INTEGER          | FK → users.id, requerido             |
| title         | VARCHAR(200)     | Requerido, min 5, max 200            |
| content       | TEXT             | Requerido                            |
| views         | INTEGER          | Por defecto `0`                      |
| rating        | DOUBLE PRECISION | Opcional, puntuación decimal         |
| published     | BOOLEAN          | Por defecto `FALSE`                  |
| published\_at | TIMESTAMP        | Nulo si no está publicado            |
| event\_date   | DATE             | Fecha de un evento relacionado       |
| created\_at   | TIMESTAMP        | Por defecto `NOW()`                  |
| updated\_at   | TIMESTAMP        | Actualiza en cada cambio             |

**Notas:**

* `user_id` enlaza el post con su autor.
* `id` usa UUID para mayor seguridad y unicidad global.
* `event_date` guarda solo fecha sin hora.
* `rating` usa precisión doble para valores decimales.

---

## 🛠️ Próximas funcionalidades de seguridad y extras

* [ ] **OAuth2 con JWT** para inicio de sesión y autenticación de endpoints.
* [ ] **Hashing de contraseñas** con `passlib`.
* [ ] **Autorización por roles** para restringir acciones.
* [ ] **Estado de cuenta** para suspender usuarios sin eliminarlos.
* [ ] **Sistema de etiquetas (tags)** para clasificar publicaciones.
* [ ] **Comentarios** asociados a publicaciones.
* [ ] **Búsqueda y filtrado avanzado** de posts.

---

## 📜 Resumen de tipos de datos usados

* **UUID** → identificador único global.
* **VARCHAR** → cadenas de longitud controlada.
* **TEXT** → texto largo sin límite definido.
* **BOOLEAN** → valores lógicos (`TRUE`/`FALSE`).
* **DATE** → fecha sin hora.
* **TIMESTAMP** → fecha y hora con zona horaria opcional.
* **SERIAL** → entero autoincremental (clave primaria).
* **INTEGER** → entero estándar.
* **FLOAT** / **DOUBLE PRECISION** → números con decimales, simple o doble precisión.

## 📋 Prerrequisitos

* Python 3.8 o superior
* PostgreSQL instalado y ejecutándose
* Git (opcional pero recomendado)

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repo>
cd mi-fastapi-project
```

### 2. Crear entorno virtual (Recomendado)

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows (git bash):
source venv/Scripts/activate
# En Linux/Mac:
source venv/bin/activate

# Desactiva entorno virtual
deactivate
```

### 3. Instalar dependencias

#### Opción A: Instalación manual

```bash
pip install "fastapi[all]"
pip install python-dotenv pydantic-settings sqlalchemy psycopg2-binary
pip install passlib[bcrypt]
```

#### Opción B: Usar requirements.txt (Recomendado)

```bash
pip install -r requirements.txt
```

#### Migraciones de la Base de datos
Instalar
```bash
pip install alembic
```

Inicializar
```bash
alembic init alembic
```

Crear la primera migración:
```bash
alembic revision --autogenerate -m "init tables"
```

Generar la migración
```bash
alembic revision --autogenerate -m "create users table"
```
Esto crea un archivo en alembic/versions/ con las instrucciones para crear tu tabla users.

Aplicar la migración a la base de datos:
```bash
alembic upgrade head
```

### 4. Configurar variables de entorno

Crear archivo `.env` en la raíz del proyecto:

```env
DATABASE_URL=postgresql://usuario:password@localhost:5432/nombre_bd
SECRET_KEY=tu_clave_secreta_aqui
HOST=127.0.0.1
PORT=8000
DEBUG=True
```

## 📦 Dependencias principales

| Librería            | Propósito                                        |
| ------------------- | ------------------------------------------------ |
| `fastapi[all]`      | Framework web principal + uvicorn + validaciones |
| `sqlalchemy`        | ORM para manejo de base de datos                 |
| `psycopg2-binary`   | Driver/adaptador para conectar con PostgreSQL    |
| `python-dotenv`     | Carga variables de entorno desde archivo `.env`  |
| `pydantic-settings` | Manejo tipado y centralizado de configuraciones  |

## 🏃‍♂️ Ejecutar el proyecto

### Levantar servidor (modo desarrollo)

Ejecuta el archivo de arranque para iniciar el servidor con los parámetros definidos en `.env`:

```bash
python run.py
```

Esto:

* Cargará configuración desde `.env` usando `pydantic-settings`
* Iniciará el servidor Uvicorn con host, puerto y modo debug según tu configuración

### Comandos útiles (si quieres levantarlo manualmente)

```bash
# Servidor con puerto personalizado
uvicorn app.main:app --reload --port 8080

# Servidor accesible desde red local
uvicorn app.main:app --reload --host 0.0.0.0
```

El servidor estará disponible en: [http://localhost:8000](http://localhost:8000) (o el puerto que configures)

## 📚 Documentación de la API

Una vez que el servidor esté ejecutándose:

* **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
* **OpenAPI Schema**: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

## 🏗️ Estructura del proyecto

```
mi-api/
├── app/
│   ├── __init__.py
│   ├── main.py             # Instancia de FastAPI y rutas
│   ├── config/
│   │   ├── __init__.py
│   │   ├── database.py     # Conexión a la base de datos
│   │   └── settings.py     # Configuración con pydantic-settings
│   ├── modules/
│   │   └── user/
│   │       ├── entity.py      # Modelos SQLAlchemy
│   │       ├── schema.py      # Schemas Pydantic
│   │       ├── repository.py  # Acceso a datos
│   │       ├── service.py     # Lógica de negocio
│   │       └── controller.py  # Endpoints
│   └── utils/
│       └── helpers.py
├── run.py                  # Punto de arranque de la app
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## 🔧 Desarrollo

### Crear migraciones (opcional, si usas Alembic)

```bash
# Inicializar migraciones
alembic init migrations

# Crear migración
alembic revision --autogenerate -m "mensaje"

# Aplicar migraciones
alembic upgrade head
```

## 🧪 Testing

```bash
# Instalar dependencias de testing
pip install pytest pytest-asyncio httpx

# Ejecutar tests
pytest
```

## 🌍 Variables de entorno recomendadas

```env
# Base de datos
DATABASE_URL=postgresql://usuario:password@localhost:5432/mi_bd

# Seguridad
SECRET_KEY=clave_super_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Servidor
HOST=127.0.0.1
PORT=8000
DEBUG=True
```

## 📝 Notas importantes

* Usa siempre entorno virtual (`venv`) para aislar dependencias
* No subir `.env` al repositorio (ya está en `.gitignore`)
* FastAPI genera documentación interactiva automáticamente
* En desarrollo, `DEBUG=True` y recarga automática (`reload`)

## 🤝 Contribuir

1. Fork del proyecto
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit (`git commit -am 'Add nueva funcionalidad'`)
4. Push (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request
