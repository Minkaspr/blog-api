# --------------------
# 🏗️ Etapa 1: Build
# --------------------
FROM python:3.11-slim AS builder

# Evitar buffering en logs
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias del sistema necesarias para psycopg2 y Alembic
RUN apt-get update && apt-get install -y \
    gcc libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# Copiar dependencias
COPY requirements.txt .

# Crear entorno virtual e instalar dependencias
RUN python -m venv /venv && /venv/bin/pip install --upgrade pip && /venv/bin/pip install -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# -------------------------------
# 🚀 Etapa 2: Imagen final (runtime)
# -------------------------------
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Instalar solo librerías mínimas necesarias en runtime
RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*

# Copiar el entorno virtual desde la etapa anterior
COPY --from=builder /venv /venv

# Copiar la aplicación
COPY . .

# Dar permisos al entrypoint
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Exponer el puerto
EXPOSE 8000

# Usar el venv para correr la app
ENV PATH="/venv/bin:$PATH"

# Ejecutar entrypoint
ENTRYPOINT ["./entrypoint.sh"]

