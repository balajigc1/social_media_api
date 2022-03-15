from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. database import get_db
from .. import schemas, models, oauth2
from passlib.context import CryptContext

router = APIRouter(tags=['Authentication'])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
# OAuth2PasswordRequestForm only supports username and password, so we need to change to return username    

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid username or password')

    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid username or password')

    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    return {"token": access_token, "token type": "bearer"}


