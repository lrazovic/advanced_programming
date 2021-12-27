from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from dataclasses import dataclass


@dataclass
class Post:
    title: str
    content: str


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "Davide"}


@app.get("/items/{item_id}")
def read_item(item_id, q=None):
    return {"item_id": item_id, "q": q}


@app.get("/api")
def read_post():
    post = Post(title="Hello", content="World")
    return JSONResponse(content=jsonable_encoder(post))
