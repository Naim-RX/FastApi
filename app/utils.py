# Imports the PasswordHash class from the pwdlib library.
from pwdlib import PasswordHash

# Creates a password hashing object using the recommended secure algorithm.
# pwdlib currently chooses a recommended password hashing configuration.
password_hash = PasswordHash.recommended()

# Defines a function that receives a plain-text password as a string.
def hash_password(password: str):

    # Hashes the plain-text password and returns the generated password hash.
    # The hash should be stored in the database instead of the original password.
    return password_hash.hash(password)