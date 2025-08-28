import subprocess
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from app.core.error_handler import setup_exception_handlers
from app.core.error_type import BaseError
from app.core.config import get_settings
from app.api.v1.router import router as api_v1_router
from app.core.database import test_connection  # Función para probar la conexión a la BD

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
  """
  Maneja el ciclo de vida de la aplicación.
  Se ejecuta al iniciar y al cerrar la aplicación.
  """
  print("🚀 Iniciando aplicación...")

  print("📋 Configuración cargada:")
  print(f"   - App: {settings.app_name}")
  print(f"   - Debug: {settings.debug}")
  print(f"   - Database URL: {settings.database_url}")

  try:
    print("🔍 Verificando conexión a la base de datos...")
    connected = test_connection()
  except Exception as e:
    print(f"❌ Error al conectar a la base de datos: {e}")
    connected = False

  if connected:
    print("📦 Aplicando migraciones con Alembic...")
    try:
      subprocess.run(["alembic", "upgrade", "head"], check=True)
      print("✅ Migraciones aplicadas correctamente")
    except subprocess.CalledProcessError as e:
      print(f"❌ Error al aplicar migraciones: {e}")
  else:
    print("⚠️ La aplicación funcionará sin BD")

  yield  # Aquí la app está funcionando

  print("🛑 Cerrando aplicación...")

# Inicialización de la aplicación FastAPI con lifespan
app = FastAPI(
  title=settings.app_name,
  debug=settings.debug,
  lifespan=lifespan  # Agregar el manejo del ciclo de vida
)

# Configuración del middleware CORS
# Esto permite que clientes desde otros dominios puedan acceder a la API.
# En producción, es recomendable restringir `allow_origins` a dominios específicos.
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],  
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# Sobrescribimos el handler de validación
setup_exception_handlers(app)

# Endpoint raíz (informativo)
@app.get("/")
async def root():
  """
  Endpoint raíz para verificar que la API está en funcionamiento.
  Devuelve un mensaje de bienvenida y el entorno actual.
  """
  return {
    "message": f"Welcome to {settings.app_name} API",
    "version": "1.0.0",
    "environment": settings.environment
  }

# Endpoint de health-check
@app.get("/health")
async def health_check():
  """
  Endpoint de verificación del estado de la API.
  Retorna un JSON indicando que el servicio está operativo.
  Puede ser usado por servicios de monitoreo.
  """
  return {
    "status": "healthy",
    "environment": settings.environment,
    "author": settings.author
  }

# Registro del router principal de la API
# `prefix` indica que todos los endpoints definidos en este router comenzarán con `/api/v1`
app.include_router(api_v1_router, prefix="/api/v1")