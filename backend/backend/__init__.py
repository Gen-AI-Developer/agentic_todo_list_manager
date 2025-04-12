from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# In-memory storage for TODO items
todos = {}
next_id = 1

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    pass

class Todo(TodoBase):
    id: int

@app.get("/")
async def read_root():
    return {"message": "Welcome to the TODO API",
            "status": "Todo API is running successfully",
            "documentation": "Visit /docs for API documentation",}
# @app.get("/docs")
# async def read_docs():
#     return {"message": "Welcome to the TODO API",
#             "post: /todos/": "To Create a new TODO item",
#             "get: /todos/": "To Read all TODO item",
#             "get: /todos/item": "To Read a specific TODO item",
#             "put: /todos/item": "To Update a specific TODO item",
#             "delete: /todos/": "To Delete a specific TODO item",
#             }

@app.post("/todos/", response_model=Todo)
async def create_todo(todo: TodoCreate):
    global next_id
    todo_item = Todo(id=next_id, **todo.dict())
    todos[next_id] = todo_item
    next_id += 1
    return todo_item

@app.get("/todos/", response_model=List[Todo])
async def read_todos():
    return list(todos.values())

@app.get("/todos/{todo_id}", response_model=Todo)
async def read_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos[todo_id]

@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo: TodoUpdate):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    updated_todo = Todo(id=todo_id, **todo.dict())
    todos[todo_id] = updated_todo
    return updated_todo

@app.delete("/todos/{todo_id}", response_model=dict)
async def delete_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos[todo_id]
    return {"detail": "Todo deleted"}