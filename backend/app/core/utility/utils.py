import pytz
from datetime import datetime
from backend.app.core import ENUM_TIMEZONE
from flask import jsonify
import base64
import cv2
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf

def get_paris_time():
    paris_tz = pytz.timezone(ENUM_TIMEZONE.TIMEZONE_PARIS.value)
    return datetime.now(paris_tz)

def convert_to_datetime(time_to_convert):
    return datetime.fromtimestamp(time_to_convert, tz=pytz.UTC)

def create_json_response(status_code=200, **kwargs):
    response = jsonify(kwargs)
    response.status_code = status_code
    return response

def preprocess_images_GAS(image_base64, img_size: tuple[int, int], needGray: bool=True) -> list:
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
    image_data = base64.b64decode(image_base64)
    image = tf.io.decode_jpeg(image_data, channels=3)
    image = tf.cast(image, tf.float32)
    image = image / 255.0
    image = tf.image.resize(image, [224, 224])
    image = tf.reshape(image, [-1, 224, 224, 3])
    return image
    