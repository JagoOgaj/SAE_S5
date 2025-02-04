from typing import Self
from backend.app.models.models import MODEL_CONVERSATION, MODEL_MESSAGE
from collections import defaultdict
from backend.app.core.utility import get_paris_time
from backend.app.services.db_service import service_db
from backend.app.exeptions.custom_exeptions import (
    ConversationNotFoundError,
    NotAllowedToAccessThisConversationError,
)
from backend.app.schemas.user_schemas import (
    ConversationMessageSchema,
    ConversationImageSchema,
)
from marshmallow import ValidationError


class Service_USER:
    def __init__(self, userId) -> None:
        self._curentUserId = userId

    def getUserConversationsByPeriod(self: Self, limit: int, page: int = 1) -> dict:
        skip_count = (page - 1) * limit
        conversations = (
            MODEL_CONVERSATION.objects(user_id=self._curentUserId)
            .order_by("-created_at")
            .skip(skip_count)
            .limit(limit)
        )
        result = defaultdict(list)
        now = get_paris_time()

        for conversation in conversations:
            delta = now - conversation.created_at
            if delta.days == 0:
                period = "Aujourd'hui"
            elif delta.days == 1:
                period = "Hier"
            elif delta.days == 2:
                period = "Avant-hier"
            elif delta.days < 7:
                period = f"Il y a {delta.days} jours"
            elif delta.days < 30:
                weeks = delta.days // 7
                period = f"Il y a {weeks} semaine{'s' if weeks > 1 else ''}"
            elif delta.days < 365:
                months = delta.days // 30
                period = f"Il y a {months} mois"
            else:
                years = delta.days // 365
                period = f"Il y a {years} an{'s' if years > 1 else ''}"

            result[period].append({"id": conversation.id, "name": conversation.name})

        return result

    def deleteConversation(self: Self, idConversation: int) -> None:
        if not isinstance(int, idConversation):
            raise TypeError("L'ID de la conversation doit être un entier")

        conversation = MODEL_CONVERSATION.objects(
            id=idConversation, user_id=self._curentUserId
        ).first()

        if not conversation:
            raise ConversationNotFoundError(idConversation)

        service_db.delete_data(conversation)

    def createConversation(self: Self, data: dict) -> None:

        conversation = MODEL_CONVERSATION(
            id=service_db.get_next_sequence_value("conversation_id"),
            user_id=self._curentUserId,
            name=data["name"],
        )

        for image in data.get("images", []):

            conversation.messages.append(
                MODEL_MESSAGE(
                    type="image",
                    content=image["image_data"],
                    created_at=image["created_at"],
                )
            )

        for msg in data.get("messages", []):

            conversation.messages.append(
                MODEL_MESSAGE(
                    type=msg["message_type"],
                    content=msg["content"],
                    created_at=msg["created_at"],
                )
            )

        service_db.add_to_db(conversation)

    def _add_messages_to_conversation(conversation: dict, messages: list):
        for message in messages:
            validated_message = ConversationMessageSchema().load(message)

            message_obj = MODEL_MESSAGE(
                type=validated_message["message_type"],
                content=validated_message["content"],
                created_at=validated_message["created_at"],
            )
            conversation.messages.append(message_obj)
        service_db.add_to_db(conversation)

    def _add_images_to_conversation(
        self: Self, conversation: MODEL_CONVERSATION, images: list
    ) -> None:
        for image in images:
            validated_image = ConversationImageSchema().load(image)

            image_obj = MODEL_MESSAGE(
                type="image",
                content=validated_image["image_data"],
                created_at=validated_image["created_at"],
            )
            conversation.messages.append(image_obj)
        service_db.add_to_db(conversation)

    def updateConversation(self: Self, data: dict, idConversation: int) -> None:
        try:
            if not isinstance(int, idConversation):
                raise TypeError("L'id de la conversation doit etre un entier")

            conversation = MODEL_CONVERSATION.objects(id=idConversation).first()

            if not conversation:
                raise ConversationNotFoundError(idConversation)

            if conversation._user_id != self._curentUserId:
                raise NotAllowedToAccessThisConversationError(idConversation)

            if "messages" in data:
                self._add_messages_to_conversation(conversation, data["messages"])

            if "images" in data:
                self._add_images_to_conversation(conversation, data["images"])

        except TypeError as e:
            raise TypeError("L'id de la conversation doit être un entier") from e

        except ConversationNotFoundError as e:
            raise ConversationNotFoundError(
                f"Conversation avec l'ID {idConversation} non trouvée."
            ) from e

        except NotAllowedToAccessThisConversationError as e:
            raise NotAllowedToAccessThisConversationError(
                "Vous n'êtes pas autorisé à accéder à cette conversation."
            ) from e

        except ValidationError as e:
            raise ValidationError(str(e)) from e

        except Exception as e:
            raise Exception(
                f"Une erreur inconnue est survenue lors de la mise à jour de la conversation : {str(e)}"
            ) from e

    def get_conversation(self: Self, idConversation: int) -> dict[str:...]:
        try:
            if not isinstance(int, idConversation):
                raise TypeError("L'id de la conversation doit etre un entier")

            conversation = MODEL_CONVERSATION.objects(id=idConversation).first()

            if not conversation:
                raise ConversationNotFoundError(idConversation)

            if conversation._user_id != self._curentUserId:
                raise NotAllowedToAccessThisConversationError(idConversation)

            messages = sorted(conversation.messages, key=lambda msg: msg.created_at)

            message_data = ConversationMessageSchema(many=True).dump(messages)

            return {
                "id": conversation.id,
                "name": conversation.name,
                "start_date": conversation.start_date,
                "messages": message_data,
            }

        except ConversationNotFoundError as e:
            raise ConversationNotFoundError(
                f"Conversation avec l'ID {idConversation} non trouvée."
            ) from e

        except NotAllowedToAccessThisConversationError as e:
            raise NotAllowedToAccessThisConversationError(
                "Vous n'êtes pas autorisé à accéder à cette conversation."
            ) from e

        except TypeError as e:
            raise TypeError("L'id de la conversation doit être un entier") from e

        except ValidationError as e:
            raise ValidationError(str(e)) from e

        except Exception as e:
            raise Exception(f"Une erreur inconnue est survenue : {str(e)}") from e
