from typing import Self
from tensorflow.keras.models import load_model
from backend.app.core.const.enum import ENUM_MODELS_TYPE
from backend.app.exeptions import ModelTypeNotFoundError
from backend.app.core.utility.utils import (
    preprocess_images_GAS,
    preprocess_images_GAT
)
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from flask import (
    request
)

class Model_CNN():
    _model = None
    _model2 = None
    def __init__(self: Self, typeModel: str) -> None:
        if typeModel not in (l:=[
            ENUM_MODELS_TYPE.GENDER_AND_AGE_SCRATCH.value, 
            ENUM_MODELS_TYPE.GENDER_SCRATCH.value, 
            ENUM_MODELS_TYPE.AGE_SCRATCH.value, 
            ENUM_MODELS_TYPE.GENDER_AND_AGE_TRANSFER.value
            ]):
            raise ModelTypeNotFoundError(self._typeModel)
        self._typeModel = typeModel

        match typeModel:
            case ENUM_MODELS_TYPE.GENDER_AND_AGE_SCRATCH.value:
                self._model = load_model(...) #TODO ADD PATH
            case ENUM_MODELS_TYPE.GENDER_SCRATCH.value:
                self._model = load_model(...) #TODO ADD PATH
            case ENUM_MODELS_TYPE.AGE_SCRATCH.value:
                self._model = load_model(...) #TODO ADD PATH
            case ENUM_MODELS_TYPE.GENDER_AND_AGE_TRANSFER.value:
                self._model = load_model(...) #TODO ADD PATH
                self._model2 = load_model(...) #TODO ADD PATH
            
    def __preprocess_image(self, imageBase64) -> list:
        if any(self._typeModel == typeModel for typeModel in [
                ENUM_MODELS_TYPE.GENDER_AND_AGE_SCRATCH.value, ENUM_MODELS_TYPE.GENDER_SCRATCH.value, ENUM_MODELS_TYPE.AGE_SCRATCH.value
            ]):
            image_size = self.__get_image_size(self._typeModel)
            return preprocess_images_GAS(imageBase64, image_size, needGray=False if 
                                  self._typeModel == ENUM_MODELS_TYPE.GENDER_AND_AGE_SCRATCH else True
            )
        elif self._typeModel == ENUM_MODELS_TYPE.GENDER_AND_AGE_TRANSFER.value:
            return preprocess_images_GAT(imageBase64)    
        else :
            raise ModelTypeNotFoundError(self._typeModel)
    
    def get_prediction(self: Self, imageBase64) -> str:
        img = self.__preprocess_image(imageBase64)
        
        match self._typeModel:
            case ENUM_MODELS_TYPE.GENDER_SCRATCH.value:
                
                value = np.argmax(self._model.predict(img))
                if value == 0:
                    return "Homme"
                elif value == 1:
                    return "Femme"
                else :
                    return "..."
                
            case ENUM_MODELS_TYPE.AGE_SCRATCH.value:
                return (
                    f"{round(MinMaxScaler().inverse_transform(
                        self._model.predict(img)
                    )[0][0])} ans"
                )
            
            case ENUM_MODELS_TYPE.GENDER_AND_AGE_SCRATCH.value:
                gender_pred, age_pred = self._model.predict(img)
                return (
                    f"{'Homme' if gender_pred[0][0] < 0.5 else 'Femme'} de 
                        {age_pred[0][0]:.2f} ans"
                )
            case ENUM_MODELS_TYPE.GENDER_AND_AGE_TRANSFER.value:
                gender_mapping = ["Homme", "Femme"]
                pred_age = tf.round(tf.squeeze(self._model.predict(img, verbose=0)), 2)
                pred_gender = tf.round(tf.squeeze(self._model2.predict(img, verbose=0)))
                return (
                    f"{gender_mapping[pred_gender]} de {int(pred_age)} ans"
                )
            case _:
                ModelTypeNotFoundError(self._typeModel)
                
    def __get_image_size(self: Self) -> tuple[int, int]:
        if self._typeModel == ENUM_MODELS_TYPE.GENDER_AND_AGE_SCRATCH.value or self._typeModel == ENUM_MODELS_TYPE.AGE_SCRATCH.value:
            return (128, 128)
        elif self._typeModel == ENUM_MODELS_TYPE.GENDER_SCRATCH.value:
            return (100, 100)
        elif self._typeModel == ENUM_MODELS_TYPE.GENDER_AND_AGE_TRANSFER.value:
            return (224, 224)
        else :
            raise ModelTypeNotFoundError(self._typeModel)
        
    
def get_quota_for_model() -> str:
    type_model = request.view_args.get('typeModel', None)
    match type_model:
        case ENUM_MODELS_TYPE.AGE_SCRATCH.value:
            return "30 per day"
        case ENUM_MODELS_TYPE.GENDER_AND_AGE_SCRATCH.value:
            return "20 per day"
        case ENUM_MODELS_TYPE.GENDER_SCRATCH.value:
            return "35 per day"
        case ENUM_MODELS_TYPE.GENDER_AND_AGE_TRANSFER.value:
            return "10 per day"
        case _:
            raise ModelTypeNotFoundError(type_model)