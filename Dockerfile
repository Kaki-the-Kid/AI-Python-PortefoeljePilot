FROM python:3.12-slim-bookworm       # Base image med Python 3.12
WORKDIR /app                         # Sæt arbejdsmappen inde i containeren
COPY requirements.txt .             # Kopiér afhængighedsfilen
RUN pip install --no-cache-dir -r requirements.txt  # Installer Python-pakker
COPY . .                             # Kopiér resten af projektet ind
EXPOSE 5000                          # Fortæl Docker at appen bruger port 5000
CMD ["python", "app.py"]            # Start Flask-appen når containeren kører