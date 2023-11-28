FROM python:3.8

WORKDIR /app

COPY requirements.txt .

# Instalar otras dependencias desde requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=app.py

CMD [ "flask", "run", "-h", "0.0.0.0"]
