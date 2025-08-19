from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
  """
  Clase para manejar las configuraciones principales de la aplicación.
  Lee automáticamente las variables de entorno desde un archivo .env.development.
  """

  # Configuración de la aplicación
  app_name: str = "BlogAPI"
  environment: str = "development"  # Entorno: development, staging, production
  debug: bool = True
  host: str = "127.0.0.1"
  port: int = 8000  

  # Configuración de la base de datos
  database_url: str = "postgresql://user:password@localhost:5432/blogdb"

  # Configuración de seguridad
  # SECRET_KEY se usa para firmar y verificar tokens JWT o cifrar datos sensibles.
  secret_key: str = "dev-secret-key"
  access_token_expire_minutes: int = 30  # Expiración de tokens en minutos

  class Config:
    # Especifica el archivo desde el cual cargar las variables de entorno
    env_file = ".env.development"
    case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
  """
  Retorna una instancia única (singleton) de las configuraciones.
  Esto evita recargar el archivo .env cada vez que se accede a la configuración.
  """
  return Settings()
