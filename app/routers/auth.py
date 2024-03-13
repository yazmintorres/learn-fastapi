from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils, oauth2

router = APIRouter(prefix="/auth", tags=["Authentication"])

#when sending data, generally a post request
@router.post("/login", response_model=schemas.Token)
def login_user(user_credentials: OAuth2PasswordRequestForm = Depends() , db: Session = Depends(get_db)):
    # 1. Get hashed password associated with email from DB
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if user is None: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail= "Invalid credentials")

    # 2. Hash the password sent by the user and verify it matches what's in DB
    authenticated = utils.verify(user_credentials.password, user.password)

    if not authenticated: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


    # 3. If a match, send back JWT token
    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}