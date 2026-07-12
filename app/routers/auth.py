from fastapi import FastAPI, HTTPException , status, Depends,APIRouter
from .. import model,schema,utils,database,oauth2
from sqlalchemy.orm import Session
from ..database import engine , get_db
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
# Creates an API router and groups the endpoint under Authentication.
router = APIRouter(
    tags=["Authentication"]
)

# Handles login requests.
@router.post("/login")
def login(
    user_credentials: OAuth2PasswordRequestForm=Depends(),
    db: Session = Depends(get_db)
):
    # Finds a user using the provided email.
    user = db.query(model.Student).filter(
        model.Student.email == user_credentials.username
    ).first()

    # Checks whether the user exists.
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Compares the plain-text login password with the stored password hash.
    if not utils.verify_password(
        user_credentials.password,
        user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Calls the create_access_token() function from the oauth2.py file.
    access_token = oauth2.create_access_token(

        # Adds the student's ID to the JWT payload as "user_id".
        data={"user_id": user.id},

        # Sets the token expiration duration using the value
        # ACCESS_TOKEN_EXPIRE_MINUTES defined in oauth2.py.
        expires_delta=timedelta(
            minutes=oauth2.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    # Temporary success response.
    return {"message":access_token, "Token type": "Bearer"}

    
