#Imagen base
FROM python:3.10

#Crear directorio de trabajo
WORKDIR /app


COPY requirements.txt /app

#Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]