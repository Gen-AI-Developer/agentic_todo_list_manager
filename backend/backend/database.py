from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./todos.db"  # Change this to your database URL
"""
The URL for the database connection. Currently set to use SQLite with a file named `todos.db`.
"""

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
"""
Creates a SQLAlchemy engine instance.

Attributes:
    DATABASE_URL (str): The URL for the database connection.
    connect_args (dict): Additional arguments for the connection. `check_same_thread=False` is used for SQLite to allow connections from multiple threads.
"""

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""
Creates a sessionmaker instance for the database.

Attributes:
    autocommit (bool): If True, the session will automatically commit transactions. Defaults to False.
    autoflush (bool): If True, the session will automatically flush before certain query operations. Defaults to False.
    bind (Engine): The engine instance to bind the session to.
"""

Base = declarative_base()
"""
Creates a base class for declarative class definitions using SQLAlchemy.
"""

def init_db():
    """
    Initializes the database by creating all tables defined in the models.

    This function imports the `models` module to ensure that all models are registered with the metadata before creating the tables.
    """
    import models  # Import models here to ensure they are registered
    Base.metadata.create_all(bind=engine)