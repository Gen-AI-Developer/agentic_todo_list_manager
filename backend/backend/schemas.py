from pydantic import BaseModel
from typing import List, Optional

class TodoBase(BaseModel):
    """
    Base schema for a Todo item.

    Attributes:
        title (str): The title of the Todo item.
        description (Optional[str]): The description of the Todo item. Defaults to None.
    """
    title: str
    description: Optional[str] = None

class TodoCreate(TodoBase):
    """
    Schema for creating a new Todo item.

    Inherits from:
        TodoBase: Base schema for a Todo item.
    """
    pass

class TodoUpdate(TodoBase):
    """
    Schema for updating an existing Todo item.

    Inherits from:
        TodoBase: Base schema for a Todo item.

    Attributes:
        completed (Optional[bool]): The completion status of the Todo item. Defaults to None.
    """
    completed: Optional[bool] = None

class Todo(TodoBase):
    """
    Schema for a Todo item with an ID and completion status.

    Inherits from:
        TodoBase: Base schema for a Todo item.

    Attributes:
        id (int): The unique identifier for the Todo item.
        completed (bool): The completion status of the Todo item.
    """
    id: int
    completed: bool

    class Config:
        """
        Configuration for the Pydantic model.

        Attributes:
            orm_mode (bool): Enables ORM mode to allow Pydantic models to read data from ORM models.
        """
        orm_mode = True

class TodoList(BaseModel):
    """
    Schema for a list of Todo items.

    Attributes:
        todos (List[Todo]): A list of Todo items.
    """
    todos: List[Todo]