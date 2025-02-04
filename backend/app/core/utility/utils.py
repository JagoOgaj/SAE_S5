import pytz
from datetime import datetime
from backend.app.core import ENUM_TIMEZONE
from flask import jsonify, request
import base64
import cv2
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
import requests
from user_agents import parse
from backend.app.log import logger


def get_paris_time():
    """
    Retourne l'heure actuelle dans le fuseau horaire de Paris.

    Returns:
        datetime: L'heure actuelle dans le fuseau horaire de Paris.
    """
    paris_tz = pytz.timezone(ENUM_TIMEZONE.TIMEZONE_PARIS.value)
    return datetime.now(paris_tz)


def convert_to_datetime(time_to_convert):
    """
    Convertit un timestamp en objet datetime dans le fuseau horaire de Paris.

    Args:
        time_to_convert (int): Le timestamp à convertir.

    Returns:
        datetime: L'objet datetime correspondant dans le fuseau horaire de Paris.
    """
    return datetime.fromtimestamp(
        time_to_convert, tz=pytz.timezone(ENUM_TIMEZONE.TIMEZONE_PARIS.value)
    )


def create_json_response(status_code=200, **kwargs):
    """
    Crée une réponse JSON avec un code de statut HTTP.

    Args:
        status_code (int, optional): Le code de statut HTTP de la réponse. Par défaut à 200.
        **kwargs: Les données à inclure dans la réponse JSON.

    Returns:
        Response: Une réponse Flask contenant les données JSON et le code de statut.
    """
    response = jsonify(kwargs)
    response.status_code = status_code
    return response


def preprocess_images_GAS(
    image_base64, img_size: tuple[int, int], needGray: bool = True
) -> list:
    """
    Prétraite une image pour l'adapter à un modèle de reconnaissance d'images.

    Args:
        image_base64 (str): L'image encodée en base64.
        img_size (tuple[int, int]): La taille à laquelle redimensionner l'image.
        needGray (bool, optional): Indique si l'image doit être convertie en niveaux de gris. Par défaut à True.

    Returns:
        list: Une liste contenant l'image prétraitée.
    """
    img_data = base64.b64decode(image_base64)
    img = Image.open(BytesIO(img_data))
    img = np.array(img)
    if needGray:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, img_size)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    if needGray:
        img = np.expand_dims(img, axis=-1)
    return img


def preprocess_images_GAT(image_base64) -> list:
    """
    Prétraite une image pour l'adapter à un modèle de reconnaissance d'images.

    Args:
        image_base64 (str): L'image encodée en base64.
        img_size (tuple[int, int]): La taille à laquelle redimensionner l'image.
        needGray (bool, optional): Indique si l'image doit être convertie en niveaux de gris. Par défaut à True.

    Returns:
        list: Une liste contenant l'image prétraitée.
    """
    image_data = base64.b64decode(image_base64)
    image = tf.io.decode_jpeg(image_data, channels=3)
    image = tf.cast(image, tf.float32)
    image = image / 255.0
    image = tf.image.resize(image, [224, 224])
    image = tf.reshape(image, [-1, 224, 224, 3])
    return image


def get_client_info():
    """
    Récupère les informations du client à partir de la requête en cours.

    Cette fonction extrait l'adresse IP du client, analyse l'en-tête User-Agent pour obtenir des informations sur l'appareil,
    et utilise un service de géolocalisation pour déterminer la région du client.

    Returns:
        tuple: Un tuple contenant l'adresse IP du client (str), la région (str) et les informations sur l'appareil (str).
    """
    client_ip = request.remote_addr
    user_agent = parse(request.headers.get("User-Agent"))
    try:
        response = requests.get(f"http://ipinfo.io/{client_ip}/json")
        region = response.json().get("region", "Unknown")
    except Exception as e:
        logger.error(f"Error fetching region info: {str(e)}")
        region = "Unknown"

    device = f"{user_agent.device.family} {user_agent.device.brand} {user_agent.device.model}"
    return client_ip, region, device
