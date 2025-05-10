import jwt
from jwt import PyJWTError
from datetime import datetime, timedelta
from . import database ,schemas,models
from fastapi import Depends,status,HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2AuthorizationCodeBearer
from .config import settings

oauth2_scheme = OAuth2AuthorizationCodeBearer(authorizationUrl='/login',tokenUrl="login")
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode=data.copy()

    expire=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})

    encoded_token=jwt.encode(to_encode, SECRET_KEY,algorithm=ALGORITHM)

    return encoded_token

def verfiy_access_token(token: str,credentials_exception):
    
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)

        id=str(payload.get('user_id'))
        if id is None:
            raise credentials_exception
        token_data=schemas.TokenData(id=id)
    except PyJWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token:str=Depends(oauth2_scheme),
                     db: Session = Depends(database.get_db)):

    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"})
    
    token = verfiy_access_token(token,credentials_exception)
    user=db.query(models.User).filter(models.User.id==token.id).first()
    return user