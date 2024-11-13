from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.status import HTTP_401_UNAUTHORIZED
import tensorflow as tf
import numpy as np
import cv2
import redis
import os
import io
from PIL import Image

# Charger le modèle TensorFlow et configurer la connexion à Redis
model = tf.keras.models.load_model('/app/model.h5')  # Charge le modèle de reconnaissance de genre stocké dans model.h5
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)  # Crée un client Redis pour gérer les quotas

# Initialiser FastAPI et la sécurité basique (HTTP Basic Auth)
app = FastAPI()  # Initialise l'application FastAPI
security = HTTPBasic()  

# Fonction pour vérifier le quota de requêtes d'un utilisateur
def check_quota(username: str):
    key = f"{username}:quota"  # Crée une clé unique pour chaque utilisateur en utilisant le nom d'utilisateur
    quota = redis_client.get(key)  # Récupère le quota actuel de l'utilisateur depuis Redis

    # Si l'utilisateur n'a pas de quota défini, on lui assigne un quota de 50 requêtes par jour
    if quota is None:
        redis_client.set(key, 50, ex=86400)  # Définit un quota de 50 avec une expiration d'un jour (86400 secondes)
        return 50

    # Si le quota est épuisé, renvoie une erreur 429
    if int(quota) <= 0:
        raise HTTPException(status_code=429, detail="Quota dépassé")

    # Diminue le quota de 1 et retourne le quota restant(on fait la meme dans la db redis)
    redis_client.decr(key)
    return int(quota) - 1

# Fonction pour charger et préparer une image pour le modèle
def load_and_prepare_image(image_data):
    image = Image.open(io.BytesIO(image_data))  
    image = image.convert("RGB") 
    face_img = np.array(image)  
    face_img = cv2.resize(face_img, (64, 64))  
    face_img = np.array(face_img).reshape(1, 64, 64, 3) / 255.0  
    return face_img







###################################################################################################################################################################
#                                                       Endpoints pour la gestion des predictions                                                                 #
###################################################################################################################################################################
# Endpoint pour la prédiction de genre
@app.post("/predict/")
async def predict_gender(credentials: HTTPBasicCredentials = Depends(security), file: UploadFile = File(...)):
    username = credentials.username  # Récupère le nom d'utilisateur
    # Vérifie le mot de passe fourni par l'utilisateur
    if credentials.password != "azerty":
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")  # Erreur si mot de passe incorrect

    check_quota(username)  # Vérifie le quota de l'utilisateur

    # Lit le fichier image téléchargé
    image_data = await file.read()
    prepared_face = load_and_prepare_image(image_data)  # Prépare l'image pour la prédiction

    # Utilise le modèle pour prédire le genre
    prediction = model.predict(prepared_face)
    predicted_class = "Femme" if prediction[0][0] > 0.5 else "Homme"  # Définit "Femme" si probabilité > 0.5, sinon "Homme"

    # Renvoie le résultat de la prédiction
    return {"prediction": predicted_class, "confidence": float(prediction[0][0])}










###################################################################################################################################################################
#                                                       Endpoints pour la gestion des utilisateurs                                                                #
###################################################################################################################################################################

# 1. Endpoint pour récupérer le quota de tous les utilisateurs
@app.get("/users/quotas/")
async def get_all_user_quotas(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != "admin" or credentials.password != "admin_password":
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid admin credentials")

    quotas = {}
    for key in redis_client.keys("*:quota"):
        username = key.split(":")[0]
        quotas[username] = int(redis_client.get(key))
    
    return {"users_quotas": quotas}

# 2. Endpoint pour récupérer le quota d'un utilisateur spécifique
@app.get("/user/{username}/quota")
async def get_user_quota(username: str, credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != "admin" or credentials.password != "admin_password":
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid admin credentials")

    key = f"{username}:quota"
    quota = redis_client.get(key)
    if quota is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"username": username, "quota": int(quota)}

# 3. Endpoint pour réinitialiser le quota d'un utilisateur
@app.post("/user/{username}/reset_quota")
async def reset_user_quota(username: str, credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != "admin" or credentials.password != "admin_password":
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid admin credentials")

    key = f"{username}:quota"
    redis_client.set(key, 50, ex=86400)  # Réinitialise le quota à 50 requêtes
    return {"username": username, "quota": 50, "message": "Quota reset successfully"}