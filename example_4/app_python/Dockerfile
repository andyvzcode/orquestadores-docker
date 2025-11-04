# Imagen oficial de Python
FROM python:3.14-slim

# Evitar buffers en logs
ENV PYTHONUNBUFFERED=1

# Crear y usar directorio de la app
WORKDIR /app

# Copiar requirements y instalarlas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Exponer el puerto que usará uvicorn
EXPOSE 8000

# Comando por defecto (uvicorn)
# fastapi run --host 0.0.0.0 --port 8000
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
