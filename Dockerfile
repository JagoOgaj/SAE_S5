# Dockerfile
FROM python:3.9

# Installation des dépendances
WORKDIR /app
#COPY ./model.h5 /app/model.h5
COPY api.py /app/api.py
RUN pip install fastapi uvicorn redis tensorflow opencv-python-headless pillow python-multipart

# Commande pour démarrer l'API
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
