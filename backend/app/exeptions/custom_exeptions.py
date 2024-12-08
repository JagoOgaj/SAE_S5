class UserNotFound(Exception):
    def __init__(self, **kwargs) -> None:
        self.filter_description: str = ", ".join(
            f"{key} = {value}" for key, value in kwargs.items()
        )
        super().__init__(
            f"Aucun utilisateur trouvé avec ces filtres : \n {self.filter_description}"
        )


class UserPasswordNotFound(Exception):
    def __init__(self, user_id) -> None:
        super().__init__(
            f"Le mot de passe ne correspond pas pour l'utilisateur id : {user_id}"
        )

class EmailAlreadyUsed(Exception):
    def __init__(self, email) -> None:
        super().__init__(
            f"L'email {email} est déjà utiliser"
        )

class PayloadError(Exception):
    def __init__(self, *args) -> None:
        self.missing_arg: str = ", ".join(f"{arg}" for arg in args)
        super().__init__(f"Un ou plusieurs champs manquant : {self.missing_arg}")

class FieldsMissingError(Exception):
    def __init__(self, message=None, details=None) -> None:
        self.message = (
            "Aucun champs n'a été renseigner pour la création"
            if message is None
            else message
        )
        self.details = "" if details is None else details
        super().__init__(f"{self.message} - \n {self.details}")

class FieldsUserMissingError(FieldsMissingError):
    def __init__(self, missing_fields):
        super().__init__(
            message="Aucun champs n' été fournis pour la création d'un utilisateur",
            details=f"Champs requis : {', '.join(missing_fields)}"
        )

class FilterMissingError(Exception):
    def __init__(self, message=None, details=None) -> None:
        self.message = (
            "Aucun filtre n'a été renseigner pour la recherche"
            if message is None
            else message
        )
        self.details = "" if details is None else details
        super().__init__(f"{self.message} - \n {self.details}")


class FilterUserMissingError(FilterMissingError):
    def __init__(self, missing_filter):
        super().__init__(
            message="Aucun filtre n'a été fournis pour la recherche d'un ou plusieurs utilisateurs",
            details=f"Filtres valables : {', '.join(missing_filter)}",
        )


class FilterTokenMissingError(FilterMissingError):
    def __init__(self, missing_filter):
        super().__init__(
            message="Aucun filtre n'a été founris pour la recherche d'un ou plusieurs tokens",
            details=f"Filtres valables : {', '.join(missing_filter)}",
        )

