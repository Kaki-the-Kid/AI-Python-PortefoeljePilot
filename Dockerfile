# Base image med Python 3.12
FROM python:3.12-slim-bookworm

# Sæt arbejdsmappen inde i containeren
WORKDIR /app                         

# Kopiér afhængighedsfilen
COPY requirements.txt .

# Installer Python-pakkerne
RUN pip install --no-cache-dir -r requirements.txt

# Kopiér resten af projektet inde i containeren
COPY . .
COPY watchdog_runner.py .

# Sæt miljøvariabler for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_PORT=5000
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Fortæl Docker at flask appen bruger port 5000
EXPOSE 5000

# Start Flask-appen når containeren kører
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--reload"]
