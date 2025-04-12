# agentic_todo_list_manager

## Overview
This project is a FastAPI application for managing a TODO list. It provides a RESTful API to create, read, update, and delete TODO items. The application is structured to separate concerns, with distinct files for models, schemas, CRUD operations, and database management.

## Project Structure
```
agentic_todo_list_manager
├── backend
│   ├── __init__.py       # Entry point of the FastAPI application with CRUD endpoints
│   ├── models.py         # Database models for TODO items
│   ├── schemas.py        # Pydantic schemas for data validation and serialization
│   ├── crud.py           # CRUD operations for TODO items
│   └── database.py       # Database connection and session management
├── tests
│   └── test_main.py      # Test cases for the FastAPI application
├── .env                  # Environment variables for the application
├── requirements.txt      # Project dependencies
└── README.md             # Documentation for the project
```

## Setup Instructions
1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd agentic_todo_list_manager
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory and add your database connection string and any other necessary environment variables.

## Usage
To run the FastAPI application, use the following command:
```
uvicorn backend.__init__:app --reload
```
You can access the API documentation at `http://127.0.0.1:8000/docs`.

## API Endpoints
- **GET /items/**: Retrieve a list of TODO items.
- **GET /items/{item_id}**: Retrieve a specific TODO item by ID.
- **POST /items/**: Create a new TODO item.
- **PUT /items/{item_id}**: Update an existing TODO item by ID.
- **DELETE /items/{item_id}**: Delete a TODO item by ID.

## Testing
To run the tests, use the following command:
```
pytest tests/test_main.py
```

## License
This project is licensed under the MIT License.