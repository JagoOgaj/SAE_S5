from typing import Self
from backend.app.core.const.enum import ENUM_MODELS_TYPE, ENUM_MODELS_ENV
from backend.app.exeptions import ModelTypeNotFoundError
import numpy as np
import tensorflow as tf
import os
from dotenv import load_dotenv
from PIL import Image
import face_recognition
import io
import cv2

load_dotenv()


class Service_MODEL:
    _model = None
    _model2 = None

    def __init__(self: Self, typeModel: str) -> None:
        if typeModel not in (
            [
                ENUM_MODELS_TYPE.GENDER_AND_AGE_SCRATCH.value,
                ENUM_MODELS_TYPE.GENDER_SCRATCH.value,
                ENUM_MODELS_TYPE.AGE_SCRATCH.value,
                ENUM_MODELS_TYPE.GENDER_AND_AGE_TRANSFER.value,
            ]
        ):
            raise ModelTypeNotFoundError(self._typeModel)
        self._typeModel = typeModel

        match typeModel:
            case ENUM_MODELS_TYPE.GENDER_AND_AGE_SCRATCH.value:
                self._model = tf.keras.models.load_model(
                    str(os.environ.get(ENUM_MODELS_ENV.PATH_GENDER_AGE_MODEL.value))
                )
            case ENUM_MODELS_TYPE.GENDER_SCRATCH.value:
                self._model = tf.keras.models.load_model(
                    str(os.environ.get(ENUM_MODELS_ENV.PATH_GENDER_MODEL.value))
                )
            case ENUM_MODELS_TYPE.AGE_SCRATCH.value:
                self._model = tf.keras.models.load_model(
                    str(os.environ.get(ENUM_MODELS_ENV.PATH_AGE_MODEL.value))
                )
            case ENUM_MODELS_TYPE.GENDER_AND_AGE_TRANSFER.value:
                self._model = tf.keras.models.load_model(
                    str(
                        os.environ.get(ENUM_MODELS_ENV.PATH_GENDER_AGE_FINETUNING.value)
                    )
                )

    def get_prediction(self: Self, imageFile) -> str:
        MAX_WIDTH = 2000  # Largeur maximale autorisée
        MAX_HEIGHT = 2000  # Hauteur maximale autorisée

        image = Image.open(io.BytesIO(imageFile.read()))

        # Vérifier la taille de l'image
        if image.width > MAX_WIDTH or image.height > MAX_HEIGHT:
            return (
                f"L'image est trop grande ({image.width}x{image.height}px). "
                f"Veuillez utiliser une image de {MAX_WIDTH}x{MAX_HEIGHT}px maximum."
            )

        face_location = self.detect_faces(image)

        if not face_location:
            return "Je n'ai détecté aucun visage sur cette image. Assurez-vous qu'il est bien visible et réessayez !"

        cropped_faces = self.crop_faces(image, face_location)
        gender_results = []
        age_results = []

        for face_image in cropped_faces:
            match self._typeModel:
                case ENUM_MODELS_TYPE.GENDER_SCRATCH.value:
                    gender, _ = self.predict_gender(face_image)
                    gender_results.append(gender)
                case ENUM_MODELS_TYPE.AGE_SCRATCH.value:
                    age, _ = self.predict_age(face_image)
                    age_results.append(age)
                case ENUM_MODELS_TYPE.GENDER_AND_AGE_SCRATCH.value:
                    gender, age = self.predict_gender_age(face_image)
                    gender_results.append(gender)
                    age_results.append(age)
                case ENUM_MODELS_TYPE.GENDER_AND_AGE_TRANSFER.value:
                    gender, age = self.predict_gender_age_transfer(face_image)
                    gender_results.append(gender)
                    age_results.append(age)
                case _:
                    raise ModelTypeNotFoundError(self._typeModel)

        num_faces = len(cropped_faces)
        avg_age = int(np.mean(age_results)) if age_results else None

        if num_faces == 1:
            message = "J'ai détecté un visage sur cette image.\n"
        else:
            message = f"J'ai trouvé {num_faces} visages sur cette image.\n"

        if gender_results:
            if num_faces == 1:
                message += f"La personne semble être un(e) {gender_results[0]}.\n"
            else:
                message += (
                    "Voici les genres détectés : " + ", ".join(gender_results) + ".\n"
                )

        if avg_age is not None:
            if num_faces == 1:
                message += f"Elle semble avoir environ {avg_age} ans.\n"
            else:
                message += (
                    f"L'âge moyen des visages détectés est d'environ {avg_age} ans.\n"
                )

        if len(gender_results) > 1:
            message += (
                f"Répartition des genres : {self.get_gender_average(gender_results)}.\n"
            )

        return message

    def get_gender_average(self, gender_results):
        """Calculer la moyenne des genres (s'il y a des genres mixtes, on peut utiliser un score de probabilité)."""
        female_count = gender_results.count("Femme")
        male_count = gender_results.count("Homme")
        total = female_count + male_count
        if total == 0:
            return "Indéfini"
        female_percentage = (female_count / total) * 100
        return (
            f"Femme : {female_percentage:.2f}%, Homme : {100 - female_percentage:.2f}%"
        )

    def ensure_8bit(self, image):
        image_array = np.array(image)
        if image_array.dtype != np.uint8:
            image_array = (image_array / (image_array.max() / 255)).astype(np.uint8)
            image = Image.fromarray(image_array, mode=image.mode)

        if image.mode not in ["RGB", "L"]:
            image = image.convert("RGB")

        return image

    def enhance_image(self, face_image):
        """Améliore la qualité de l'image : réduction du bruit, augmentation des détails, correction de contraste."""
        image = np.array(face_image)

        denoised = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)

        lab = cv2.cvtColor(denoised, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        lab = cv2.merge((l, a, b))
        contrast_enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)

        enhanced = cv2.detailEnhance(contrast_enhanced, sigma_s=10, sigma_r=0.15)

        gaussian_blurred = cv2.GaussianBlur(enhanced, (9, 9), 10.0)
        sharpened = cv2.addWeighted(enhanced, 1.5, gaussian_blurred, -0.5, 0)

        gamma = 1.2
        gamma_corrected = np.array(255 * (sharpened / 255) ** gamma, dtype="uint8")

        return Image.fromarray(gamma_corrected)

    def detect_faces(self, image):
        image = self.ensure_8bit(image)
        image_array = np.array(image)
        face_locations = face_recognition.face_locations(image_array)
        return face_locations

    def crop_faces(
        self, image, face_locations, target_size=(200, 200), margin_ratio=0.1
    ):
        cropped_faces = []
        img_width, img_height = image.size

        for i, (top, right, bottom, left) in enumerate(face_locations):
            face_width = right - left
            face_height = bottom - top

            margin_width = int(face_width * margin_ratio)
            margin_height = int(face_height * margin_ratio)

            new_left = max(0, left - margin_width)
            new_top = max(0, top - margin_height)
            new_right = min(img_width, right + margin_width)
            new_bottom = min(img_height, bottom + margin_height)

            face_image = image.crop((new_left, new_top, new_right, new_bottom))
            face_image = face_image.resize(target_size, Image.Resampling.LANCZOS)
            face_image = self.enhance_image(face_image)

            cropped_faces.append(face_image)

        return cropped_faces

    def preprocess_gender(self, face_image):
        image_gray = face_image.convert("L").resize((100, 100))
        image_array = np.array(image_gray) / 255.0
        return np.expand_dims(np.expand_dims(image_array, axis=0), axis=-1)

    def preprocess_age(self, face_image):
        image_gray = face_image.convert("L").resize((128, 128))
        image_array = np.array(image_gray) / 255.0
        return np.expand_dims(np.expand_dims(image_array, axis=0), axis=-1)

    def preprocess_gender_age(self, face_image):
        image_gray = face_image.convert("L").resize((128, 128))
        image_array = np.array(image_gray) / 255.0
        return np.expand_dims(np.expand_dims(image_array, axis=0), axis=-1)

    def preprocess_gender_age_transfer(self, face_image):
        image_rgb = face_image.convert("RGB").resize((64, 64))
        image_array = np.array(image_rgb) / 255.0
        return np.expand_dims(image_array, axis=0)

    def predict_gender(self, face_image):
        processed_image = self.preprocess_gender(face_image)
        prediction = self._model.predict(processed_image)
        return "Homme" if prediction[0][0] > 0.5 else "Femme", float(prediction[0][0])

    def predict_age(self, face_image):
        processed_image = self.preprocess_age(face_image)
        prediction = self._model.predict(processed_image)
        return int(round(prediction[0][0] * 100)), float(prediction[0][0])

    def predict_gender_age(self, face_image):
        processed_image = self.preprocess_gender_age(face_image)
        prediction = self._model.predict(processed_image)
        gender = "Homme" if prediction[0][0] < 0.5 else "Femme"
        age = int(round(float(prediction[1][0])))
        return gender, age

    def predict_gender_age_transfer(self, face_image):
        processed_image = self.preprocess_gender_age_transfer(face_image)
        prediction = self._model.predict(processed_image)
        gender = "Homme" if prediction[0][0] < 0.5 else "Femme"
        age = int(round(float(prediction[1][0]) * 100))
        return gender, age
