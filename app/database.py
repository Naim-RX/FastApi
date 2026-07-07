# The Engine is SQLAlchemy's core object that knows how to communicate with the database.
from sqlalchemy import create_engine
# sessionmaker,A factory that creates database sessions. declarative_base,Creates a base class for every SQLAlchemy model.
from sqlalchemy.orm import  sessionmaker,declarative_base

DATABASE_URL = "mysql+pymysql://root:naim.123@localhost:3306/college"

# This creates the SQLAlchemy Engine.
# contains:
# connection pool
# database dialect
# driver information
# SQL compiler
engine = create_engine(DATABASE_URL)

# This line creates a session factory.It does not create a session
#bind=engine,Every session produced by this factory will use this engine.
# autocommit=False,SQLAlchemy doesn't automatically save changes.
# autoflush=False,Before every query, SQLAlchemy can automatically synchronize pending changes with the database.
SessionLocal = sessionmaker(autocommit = False,autoflush=False,bind=engine) 

# This creates the base class for all models.
Base = declarative_base()

# This function provides a database session for each request.
def get_db():
    # is the factory.
    db = SessionLocal()
    # Everything inside your endpoint runs here.
    try:
        yield db
    finally:
        db.close()