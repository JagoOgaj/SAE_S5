from typing import Self
from backend.app.models.models import (
    Model_CONVERSATION,
    Model_CONVERSATION_IMAGES,
    Model_CONVERSATION_MESSAGE
)
from sqlalchemy import asc
from backend.app.services.db_service import service_db
from backend.app.exeptions.custom_exeptions import (
    ConversationNotFoundError,
    ConversationImagesNotFound,
    ConversationMessagesNotFound,
    NotAllowedToAccessThisConversationError
)
from backend.app.schemas.user_schemas import (
    ConversationMessageSchema,
    ConversationImageSchema
)
from marshmallow import (
    ValidationError
)

class Service_USER:
    def __init__(self, userId) -> None:
        self._curentUserId = userId
        
    def getUserConversationsOverviewPaginate(self : Self, page: int, per_page: int) -> list:
        
        query = Model_CONVERSATION.query.filter_by(
                _user_id=self._curentUserId
            ).order_by(
                asc(Model_CONVERSATION._start_date)
            )
        
        data_paginate = query.paginate(page=page, per_page=per_page, error_out=False)
        return data_paginate
        
    def deleteConversation(self: Self, idConversation: int) -> None:
        if not isinstance(int, idConversation):
            raise TypeError("L'ID de la conversation doit être un entier")
        conversation = Model_CONVERSATION.query.filter_by(id=idConversation, _user_id=self._curentUserId).first()
        
        if not conversation:
            raise ConversationNotFoundError(idConversation)
        
        messages = Model_CONVERSATION_MESSAGE.query.filter_by(_conversation_id=conversation.id).all()
        
        if not messages:
            raise ConversationMessagesNotFound(idConversation)

        for message in messages:
            service_db.delete_data(message)
        
        images = Model_CONVERSATION_IMAGES.query.filter_by(_conversation_id=conversation.id).all()
        
        if not images:
            raise ConversationImagesNotFound(idConversation)
        
        for image in images:
            service_db.delete_data(image)
        
        service_db.delete_data(conversation)
        
        service_db.commit_to_db()
        
    def createConversation(self : Self, data: dict) -> None:
        
        conversation = Model_CONVERSATION(
            _user_id=self._curentUserId,
            _name=data['name']
        )
        
        service_db.add_to_db(conversation)
        service_db.commit_to_db()
        
        for image in data["images"]:
            conversation_image = Model_CONVERSATION_IMAGES(
                _conversation_id=conversation.id,
                _image_data=image["image_data"],
                _image_size=image["image_size"],
                _created_at=image["created_at"]
            )
            service_db.add_to_db(conversation_image)

        for msg in data["messages"]:
            conversation_message = Model_CONVERSATION_MESSAGE(
                _conversation_id=conversation.id,
                _message_type=msg["message_type"],
                _content=msg["content"],
                _created_at=msg["created_at"]
            )
            service_db.add_to_db(conversation_message)

        service_db.commit_to_db()
    
    def _add_messages_to_conversation(conversation: dict, messages: list):
        for message in messages:
            validated_message = ConversationMessageSchema().load(message)
            message_obj = Model_CONVERSATION_MESSAGE(
                _conversation_id=conversation.id,
                _message_type=validated_message['message_type'],
                _content=validated_message['content'],
                _created_at=validated_message['created_at']
            )
            conversation.messages.append(message_obj)

    def _add_images_to_conversation(conversation: dict, images: list):
        for image in images:
            validated_image = ConversationImageSchema().load(image)
            image_obj = Model_CONVERSATION_IMAGES(
                _conversation_id=conversation.id,
                _image_data=validated_image['image_data'],
                _image_size=validated_image['image_size'],
                _created_at=validated_image['created_at']
            )
            conversation.images.append(image_obj)
    
    def updateConversation(self: Self, data: dict, idConversation: int) -> None:
        try :
            if not isinstance(int, idConversation):
                raise TypeError("L'id de la conversation doit etre un entier")
            
            conversation = Model_CONVERSATION.query.get(idConversation)

            if not conversation:
                raise ConversationNotFoundError(idConversation)
            
            if conversation._user_id != self._curentUserId:
                raise NotAllowedToAccessThisConversationError(idConversation)

            if 'messages' in data:
                self._add_messages_to_conversation(conversation, data['messages'])

            if 'images' in data:
                self._add_images_to_conversation(conversation, data['images'])
            
            service_db.commit_to_db()
            
        except TypeError as e:
            raise TypeError("L'id de la conversation doit être un entier") from e

        except ConversationNotFoundError as e:
            raise ConversationNotFoundError(f"Conversation avec l'ID {idConversation} non trouvée.") from e

        except NotAllowedToAccessThisConversationError as e:
            raise NotAllowedToAccessThisConversationError("Vous n'êtes pas autorisé à accéder à cette conversation.") from e

        except ValidationError as e:
            raise ValidationError(str(e)) from e

        except Exception as e:
            raise Exception(f"Une erreur inconnue est survenue lors de la mise à jour de la conversation : {str(e)}") from e
    
    def get_conversation(self: Self, idConversation: int) -> dict[str : ...]:
        try :
            if not isinstance(int, idConversation):
                raise TypeError("L'id de la conversation doit etre un entier")
            
            conversation = Model_CONVERSATION.query.get(idConversation)
            
            if not conversation:
                raise ConversationNotFoundError(idConversation)
            
            if conversation._user_id != self._curentUserId:
                raise NotAllowedToAccessThisConversationError(idConversation)
            
            
            messages = sorted(conversation.messages, key=lambda msg: msg.created_at)
            images = sorted(conversation.images, key=lambda img: img.created_at)
            
            message_data = ConversationMessageSchema(many=True).dump(messages)
            image_data = ConversationImageSchema(many=True).dump(images)
            
            return {
                "id": conversation.id,
                "name": conversation.name,
                "start_date": conversation.start_date,
                "messages": message_data,
                "images": image_data
            }
            
        except ConversationNotFoundError as e:
            raise ConversationNotFoundError(f"Conversation avec l'ID {idConversation} non trouvée.") from e
    
        except NotAllowedToAccessThisConversationError as e:
            raise NotAllowedToAccessThisConversationError("Vous n'êtes pas autorisé à accéder à cette conversation.") from e
        
        except TypeError as e:
            raise TypeError("L'id de la conversation doit être un entier") from e
        
        except ValidationError as e:
            raise ValidationError(str(e)) from e
        
        except Exception as e:
            raise Exception(f"Une erreur inconnue est survenue : {str(e)}") from e
