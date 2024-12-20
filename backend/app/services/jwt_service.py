from backend.app.models.models import Model_TOKEN_BLOCK_LIST
from flask_jwt_extended import decode_token
from backend.app.core.const.enum import ENUM_DECODED_TOKEN_KEY, ENUM_JWT_ENV
from flask import app as SAE_S5_BACKEND
from datetime import datetime
from backend.app.services.db_service import service_db
from backend.app.core.decorator.decorators import Decorators
from backend.app.core.utility.utils import get_paris_time, convert_to_datetime
from sqlalchemy.exc import NoResultFound
from backend.app.extension.extensions import ext


class Service_JWT:
    def __init__(self) -> None:
        pass

    def add_token_to_database(self, encoded_token: str) -> None:
        decoded_token = decode_token(encoded_token)

        db_token = Model_TOKEN_BLOCK_LIST(
            jti=decoded_token[ENUM_DECODED_TOKEN_KEY.JTI.value],
            token_type=decoded_token[ENUM_DECODED_TOKEN_KEY.TYPE.value],
            user_id=decoded_token[
                SAE_S5_BACKEND.config.get(ENUM_JWT_ENV.IDENTITY_CLAIM.value)
            ],
            expires=datetime.fromtimestamp(
                decoded_token[ENUM_DECODED_TOKEN_KEY.EXP.value]
            ),
        )

        service_db.add_to_db(db_token)
        service_db.commit_to_db()

    def revoke_token(token_jti, user_id) -> None:
        try:
            token = service_db.find_token_by_filters(jti=token_jti, user_id=user_id)
            token.revoked_at = get_paris_time()
            service_db.commit_to_db()

        except NoResultFound as e:
            raise NoResultFound(f"Aucun token trouver avec token_jti = {token_jti}, user_id = {user_id} - \n {e}")
            

        except Exception as e:
            raise Exception(f"Une erreur est survenu - \n {e}")

    def is_token_revoked(jwt_payload) -> bool:
        jti = jwt_payload[ENUM_DECODED_TOKEN_KEY.JTI.value]
        user_id = jwt_payload[
            SAE_S5_BACKEND.config.get(ENUM_JWT_ENV.IDENTITY_CLAIM.value)
        ]

        try:
            token = service_db.find_token_by_filters(jti=jti, user_id=user_id)
            return token.revoked_at is not None

        except NoResultFound as e:
            print(f"Aucun token trouver avec jti = {jti}, user_id = {user_id} - \n {e}")

        except Exception as e:
            print(f"Une erreur est survenu - \n {e}")

    def is_token_expired(expiration_timestamp) -> bool:
        if expiration_timestamp is None:
            return False

        expiration_time = convert_to_datetime(expiration_timestamp)
        curent_time = get_paris_time()

        return expiration_time < curent_time


service_jwt: Service_JWT = Service_JWT()


@ext.jwt_ext.token_in_blocklist_loader
def check_if_token_revoked(jwt_headers, jwt_payload):
    try:
        if service_jwt.is_token_revoked(jwt_payload):
            return True

        if service_jwt.is_token_expired(jwt_payload[ENUM_DECODED_TOKEN_KEY.EXP.value]):
            service_jwt.revoke_token(
                jwt_payload[ENUM_DECODED_TOKEN_KEY.JTI.value],
                jwt_payload[
                    SAE_S5_BACKEND.config.get(ENUM_JWT_ENV.IDENTITY_CLAIM.value)
                ],
            )
            return True

        return False
    except Exception:
        return True

@ext.jwt_ext.user_lookup_loader
def user_loader_callback(jwt_header, jwt_payload):
    return service_db.find_user_by_filters(id=jwt_payload[
                    SAE_S5_BACKEND.config.get(ENUM_JWT_ENV.IDENTITY_CLAIM.value)
                ])