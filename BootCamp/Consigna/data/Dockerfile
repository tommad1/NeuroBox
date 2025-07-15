FROM python:3.9-slim

WORKDIR /app

# Copiar los archivos necesarios al contenedor
COPY ./app /app
COPY ./model /model
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7860

# Comando para iniciar la app
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=7860"]

