from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}") 
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/items/")
def read_items(q: str = None):
    return {"q": q}

@app.get("/items/{item_id}/details")
def read_item_details(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}