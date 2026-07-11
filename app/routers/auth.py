from fastapi import FastAPI, HTTPException , status, Depends,APIRouter
from .. import model,schema,utils,database
from sqlalchemy.orm import Session
from ..database import engine , get_db

# Creates an API router and groups the endpoint under Authentication.
router = APIRouter(
    tags=["Authentication"]
)

# Handles login requests.
@router.post("/login")
def login(
    user_credentials: schema.UserLogin,
    db: Session = Depends(get_db)
):
    # Finds a user using the provided email.
    user = db.query(model.Student).filter(
        model.Student.email == user_credentials.email
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

    # Temporary success response.
    return {"message": "Successfully logged in"}