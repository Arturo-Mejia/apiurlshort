# Utilizar una imagen base de Python 3.11.3
FROM python:3.11.3

# Instala las dependencias del sistema
RUN apt-get update && \
    apt-get install -y unixodbc-dev unixodbc-dev && \
    apt-get clean

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Copiar el archivo de requerimientos al directorio de trabajo
COPY requirements.txt .

# Instalar las dependencias de Python
RUN pip install Flask pyodbc gunicorn uvicorn

# Copiar el código fuente de la aplicación al directorio de trabajo
COPY . .

CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]