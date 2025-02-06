class UserNotFound(Exception):
    """
    Exception levée lorsque l'utilisateur n'est pas trouvé.

    Attributes:
        email (str): L'email de l'utilisateur non trouvé.
    """

    def __init__(self, **kwargs) -> None:
        self.filter_description: str = ", ".join(
            f"{key} = {value}" for key, value in kwargs.items()
        )
        super().__init__(
            f"Aucun utilisateur trouvé avec ces filtres : {self.filter_description}"
        )


class UserPasswordNotFound(Exception):
    """
    Exception levée lorsque le mot de passe de l'utilisateur ne correspond pas.

    Attributes:
        user_id (int): L'ID de l'utilisateur dont le mot de passe ne correspond pas.
    """

    def __init__(self, user_id) -> None:
        super().__init__(
            f"Le mot de passe ne correspond pas pour l'utilisateur id : {user_id}"
        )


class EmailAlreadyUsed(Exception):
    """
    Exception levée lorsque l'email est déjà utilisé.

    Attributes:
        email (str): L'email déjà utilisé.
    """

    def __init__(self, email) -> None:
        super().__init__(f"L'email {email} est déjà utiliser")


class PayloadError(Exception):
    """
    Exception levée lorsque la payload est invalide.

    Attributes:
        missing_fields (list): Liste des champs manquants dans la payload.
    """

    def __init__(self, *args) -> None:
        self.missing_arg: str = ", ".join(f"{arg}" for arg in args)
        super().__init__(f"Un ou plusieurs champs manquant : {self.missing_arg}")


class FieldsMissingError(Exception):
    """
    Exception levée lorsque des champs requis sont manquants pour la création.

    Attributes:
        message (str): Message d'erreur.
        details (str): Détails supplémentaires sur l'erreur.
    """

    def __init__(self, message=None, details=None) -> None:
        self.message = (
            "Aucun champs n'a été renseigner pour la création"
            if message is None
            else message
        )
        self.details = "" if details is None else details
        super().__init__(f"{self.message} - \n {self.details}")


class FieldsUserMissingError(FieldsMissingError):
    """
    Exception levée lorsque des champs requis sont manquants pour la création d'un utilisateur.

    Attributes:
        message (str): Message d'erreur.
        details (str): Détails supplémentaires sur l'erreur.
    """

    def __init__(self, missing_fields):
        super().__init__(
            message="Aucun champs n' été fournis pour la création d'un utilisateur",
            details=f"Champs requis : {', '.join(missing_fields)}",
        )


class FilterMissingError(Exception):
    """
    Exception levée lorsque des filtres requis sont manquants pour la recherche.

    Attributes:
        message (str): Message d'erreur.
        details (str): Détails supplémentaires sur l'erreur.
    """

    def __init__(self, message=None, details=None) -> None:
        self.message = (
            "Aucun filtre n'a été renseigner pour la recherche"
            if message is None
            else message
        )
        self.details = "" if details is None else details
        super().__init__(f"{self.message} - {self.details}")


class FilterUserMissingError(FilterMissingError):
    """
    Exception levée lorsque des filtres requis sont manquants pour la recherche d'un ou plusieurs utilisateurs.

    Attributes:
        message (str): Message d'erreur.
        details (str): Détails supplémentaires sur l'erreur.
    """

    def __init__(self, missing_filter):
        super().__init__(
            message="Aucun filtre n'a été fournis pour la recherche d'un ou plusieurs utilisateurs",
            details=f"Filtres valables : {', '.join(missing_filter)}",
        )


class FilterTokenMissingError(FilterMissingError):
    """
    Exception levée lorsque des filtres requis sont manquants pour la recherche d'un ou plusieurs tokens.

    Attributes:
        message (str): Message d'erreur.
        details (str): Détails supplémentaires sur l'erreur.
    """

    def __init__(self, missing_filter):
        super().__init__(
            message="Aucun filtre n'a été founris pour la recherche d'un ou plusieurs tokens",
            details=f"Filtres valables : {', '.join(missing_filter)}",
        )


class ModelTypeNotFoundError(Exception):
    """
    Exception levée lorsque le type de modèle n'est pas trouvé.

    Attributes:
        modelType (str): Le type de modèle non trouvé.
    """

    def __init__(self, modelType: str) -> None:
        super().__init__(
            f"Ce type de model '{modelType}' ne correspond à aucun type connue"
        )


class ConversationNotFoundError(Exception):
    """
    Exception levée lorsque la conversation n'est pas trouvée.

    Attributes:
        conversation_id (int): L'ID de la conversation non trouvée.
    """

    def __init__(self, conversationId: int) -> None:
        super().__init__(
            f"L'id fournis {conversationId} ne correspond à aucune conversation"
        )


class ConversationMessagesNotFound(Exception):
    """
    Exception levée lorsqu'aucun message n'est trouvé pour une conversation.

    Attributes:
        conversation_id (int): L'ID de la conversation pour laquelle aucun message n'est trouvé.
    """

    def __init__(self, conversatationId: int) -> None:
        super().__init__(
            f"Aucun message trouvée pour la conversation {conversatationId}"
        )


class ConversationImagesNotFound(Exception):
    """
    Exception levée lorsqu'aucune image n'est trouvée pour une conversation.

    Attributes:
        conversation_id (int): L'ID de la conversation pour laquelle aucune image n'est trouvée.
    """

    def __init__(self, conversationId: int) -> None:
        super().__init__(f"Aucune image trouvée pour la conversation {conversationId}")


class NotAllowedToAccessThisConversationError(Exception):
    """
    Initialise l'exception avec l'ID de la conversation à laquelle l'accès est refusé.

    Args:
        conversation_id (int): L'ID de la conversation à laquelle l'accès est refusé.
    """

    def __init__(self, conversationId: int) -> None:
        super().__init__(
            f"Vous ne pouvez pas accéder à la conversation id = {conversationId} car ce n'est pas la votre"
        )
