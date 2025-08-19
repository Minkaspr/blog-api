import uvicorn
from app.core.config import get_settings

# Cargar configuración desde .env usando Pydantic Settings
settings = get_settings()

if __name__ == "__main__":
  # Ejecuta el servidor Uvicorn con los parámetros definidos en settings
  # "app.main:app" → módulo app.main, variable app (instancia de FastAPI)
  uvicorn.run(
    "app.main:app",
    host=settings.host,      # Dirección en la que escucha
    port=settings.port,      # Puerto de la API
    reload=settings.debug    # Recarga automática en desarrollo
  )