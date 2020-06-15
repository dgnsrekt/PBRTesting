from fastapi import FastAPI
from pbrtesting.schema import Item
import uvicorn
import random

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("echo/{name}")
def echo(name: str):
    return {"name": name}


# class Item(pydantic.BaseModel):
#     name: str
#     price: float
#     is_offer: bool = None
#
@app.get("item/{item_name}")
def echo(item_name: str):
    name = item_name
    price = float(random.randint())


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, reload=True)
