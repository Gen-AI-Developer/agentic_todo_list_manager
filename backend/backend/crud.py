from sqlalchemy.orm import Session
from .models import Todo
from .schemas import TodoCreate, TodoUpdate

def create_todo(db: Session, todo: TodoCreate):
    """
    Creates a new Todo item in the database.

    Args:
        db (Session): The database session.
        todo (TodoCreate): The schema containing the data for the new Todo item.

    Returns:
        Todo: The created Todo item.
    """
    db_todo = Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def get_todo(db: Session, todo_id: int):
    """
    Retrieves a Todo item by its ID.

    Args:
        db (Session): The database session.
        todo_id (int): The ID of the Todo item to retrieve.

    Returns:
        Todo: The retrieved Todo item, or None if not found.
    """
    return db.query(Todo).filter(Todo.id == todo_id).first()

def get_todos(db: Session, skip: int = 0, limit: int = 10):
    """
    Retrieves a list of Todo items with pagination.

    Args:
        db (Session): The database session.
        skip (int, optional): The number of items to skip. Defaults to 0.
        limit (int, optional): The maximum number of items to return. Defaults to 10.

    Returns:
        List[Todo]: A list of Todo items.
    """
    return db.query(Todo).offset(skip).limit(limit).all()

def update_todo(db: Session, todo_id: int, todo: TodoUpdate):
    """
    Updates an existing Todo item in the database.

    Args:
        db (Session): The database session.
        todo_id (int): The ID of the Todo item to update.
        todo (TodoUpdate): The schema containing the data to update the Todo item.

    Returns:
        Todo: The updated Todo item, or None if not found.
    """
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo:
        for key, value in todo.dict(exclude_unset=True).items():
            setattr(db_todo, key, value)
        db.commit()
        db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: int):
    """
    Deletes a Todo item from the database.

    Args:
        db (Session): The database session.
        todo_id (int): The ID of the Todo item to delete.

    Returns:
        Todo: The deleted Todo item, or None if not found.
    """
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
    return db_todo