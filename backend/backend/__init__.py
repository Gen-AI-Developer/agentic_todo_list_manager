from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# In-memory storage for TODO items
todos = {}
next_id = 1

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
    """
    pass

class Todo(TodoBase):
    """
    Schema for a Todo item with an ID.

    Inherits from:
        TodoBase: Base schema for a Todo item.

    Attributes:
        id (int): The unique identifier for the Todo item.
    """
    id: int

@app.get("/")
async def read_root():
    """
    Root endpoint that returns a welcome message and API status.

    Returns:
        dict: A dictionary containing a welcome message, API status, and documentation link.
    """
    return {
        "message": "Welcome to the TODO API",
        "status": "Todo API is running successfully",
        "documentation": "Visit /docs for API documentation",
    }

@app.post("/todos/", response_model=Todo)
async def create_todo(todo: TodoCreate):
    """
    Endpoint to create a new Todo item.

    Args:
        todo (TodoCreate): The schema containing the data for the new Todo item.

    Returns:
        Todo: The created Todo item.
    """
    global next_id
    todo_item = Todo(id=next_id, **todo.dict())
    todos[next_id] = todo_item
    next_id += 1
    return todo_item

@app.get("/todos/", response_model=List[Todo])
async def read_todos():
    """
    Endpoint to read all Todo items.

    Returns:
        List[Todo]: A list of all Todo items.
    """
    return list(todos.values())

@app.get("/todos/{todo_id}", response_model=Todo)
async def read_todo(todo_id: int):
    """
    Endpoint to read a specific Todo item by its ID.

    Args:
        todo_id (int): The ID of the Todo item to retrieve.

    Returns:
        Todo: The retrieved Todo item.

    Raises:
        HTTPException: If the Todo item is not found.
    """
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos[todo_id]

@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo: TodoUpdate):
    """
    Endpoint to update an existing Todo item by its ID.

    Args:
        todo_id (int): The ID of the Todo item to update.
        todo (TodoUpdate): The schema containing the data to update the Todo item.

    Returns:
        Todo: The updated Todo item.

    Raises:
        HTTPException: If the Todo item is not found.
    """
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    updated_todo = Todo(id=todo_id, **todo.dict())
    todos[todo_id] = updated_todo
    return updated_todo

@app.delete("/todos/{todo_id}", response_model=dict)
async def delete_todo(todo_id: int):
    """
    Endpoint to delete a specific Todo item by its ID.

    Args:
        todo_id (int): The ID of the Todo item to delete.

    Returns:
        dict: A dictionary containing a detail message indicating the Todo item was deleted.

    Raises:
        HTTPException: If the Todo item is not found.
    """
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos[todo_id]
    return {"detail": "Todo deleted"}