from backend.app.models.models import (
    Model_USER
)
from backend.app.extension import ext

def login(data: dict[... : ...]):
    if (email:=data.get("email")) and (password:=data.get("password")):
        
        user = Model_USER.query.filter(_email=email).first()
        
        if not user:
            raise Exception("Aucun utilisateur trouver")    
        
        else :
            if not ext.pwd_context_ext.verify(password, user.password_hash):
                raise Exception("Le mot de passe ne correspond pas")
                
            else :
                if user.is_admin:
                    ... # Login admin
                # Login classique user
    else:
        raise Exception()
    
    
    
