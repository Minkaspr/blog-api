from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Generator
from app.core.config import get_settings

settings = get_settings()

# Crear el motor de conexión
engine = create_engine(settings.database_url)

# Crear una clase Base para que tus modelos hereden de ella
Base = declarative_base()

# Crear una clase SessionLocal para instanciar sesiones con la BD
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

def get_db() -> Generator[Session, None, None]:
  """
  Dependencia para obtener una sesión de base de datos.
  """
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

def test_connection() -> bool:
  """
  Prueba la conexión a la base de datos y muestra el resultado por consola.
  Compatible con SQLAlchemy 2.x.
  Devuelve True si conexión exitosa, False si falla.
  """
  try:
    with engine.connect() as connection:
      connection.execute(text("SELECT 1"))
    print("✅ Conexión exitosa a la base de datos")
    return True
  except OperationalError as e:
    print("❌ Error al conectar a la base de datos:")
    print(e)
    return False


if __name__ == "__main__":
  test_connection()
