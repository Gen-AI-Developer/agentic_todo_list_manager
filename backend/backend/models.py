from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

# Create a base class for declarative class definitions
Base = declarative_base()

class Todo(Base):
    """
    Represents a Todo item in the database.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        id (int): The unique identifier for the Todo item.
        title (str): The title of the Todo item.
        description (str): The description of the Todo item.
        completed (bool): The completion status of the Todo item.
    """
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    """
    The unique identifier for the Todo item.

    Attributes:
        Integer: The data type of the column.
        primary_key (bool): Indicates that this column is the primary key.
        index (bool): Indicates that this column is indexed for faster lookups.
    """

    title = Column(String, index=True)
    """
    The title of the Todo item.

    Attributes:
        String: The data type of the column.
        index (bool): Indicates that this column is indexed for faster lookups.
    """

    description = Column(String, default="")
    """
    The description of the Todo item.

    Attributes:
        String: The data type of the column.
        default (str): The default value for the column if no value is provided.
    """

    completed = Column(Boolean, default=False)
    """
    The completion status of the Todo item.

    Attributes:
        Boolean: The data type of the column.
        default (bool): The default value for the column if no value is provided.
    """