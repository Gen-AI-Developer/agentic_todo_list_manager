from pydantic import BaseModel
from typing import List, Optional

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    completed: Optional[bool] = None

class Todo(TodoBase):
    id: int
    completed: bool

    class Config:
        orm_mode = True

class TodoList(BaseModel):
    todos: List[Todo]