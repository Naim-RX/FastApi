# Imports the jwt library used to create and encode JSON Web Tokens.
import jwt

# Imports datetime for current date/time,
# timedelta for adding time durations,
# and timezone for working with UTC time.
from datetime import datetime, timedelta, timezone


# Secret key used to digitally sign the JWT token.
# The same key is required later to verify and decode the token.
# In a real project, store this in an environment variable instead of source code.
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"


# Defines the cryptographic algorithm used to sign the JWT token.
ALGORITHM = "HS256"


# Defines how long an access token should remain valid in minutes.
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Defines a function for creating a JWT access token.
# data contains the information that will be stored inside the token.
# expires_delta allows a custom token expiration duration.
def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
):

    # Creates a copy of the original data dictionary.
    # This prevents modification of the original dictionary.
    to_encode = data.copy()


    # Checks whether a custom expiration duration was provided.
    if expires_delta:

        # Gets the current UTC time and adds the custom expiration duration.
        expire = datetime.now(timezone.utc) + expires_delta

    else:

        # If no custom expiration duration is provided,
        # the token will expire after 15 minutes.
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)


    # Adds the expiration time to the JWT payload.
    # "exp" is a standard JWT expiration claim.
    to_encode.update({"exp": expire})


    # Creates and digitally signs the JWT token.
    # to_encode is the token payload.
    # SECRET_KEY signs the token.
    # ALGORITHM defines the signing algorithm.
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


    # Returns the generated JWT access token.
    return encoded_jwt