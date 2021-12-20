from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "Davide"}


@app.get("/items/{item_id}")
def read_item(item_id, q = None):
    return {"item_id": item_id, "q": q}