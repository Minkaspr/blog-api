echo "📦 Aplicando migraciones con Alembic..."
alembic upgrade head

echo "🚀 Iniciando API..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000