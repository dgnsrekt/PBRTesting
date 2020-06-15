from fastapi import FastAPI
from pbrtesting.schema import Item
from decouple import config
import uvicorn
import random

app = FastAPI()


@app.get("/")
def read_root():
    """Returns Hello World"""
    return {"Hello": "World"}


@app.get("/echo/{name}")
def echo(name: str):
    """Echos Name"""
    return {"name": name.title()}


@app.get("/item/{item_name}")
def get_item(item_name: str):
    """Gets Item by item_name"""
    name = item_name.title()
    price = float(random.randint(0, 4096))
    return Item(name=name, price=price)


@app.post("/item/{item_name}")
def add_item(item_name: str, price: int):
    """Adds Item"""
    name = item_name.title()
    return Item(name=name, price=price)


if __name__ == "__main__":
    uvicorn.run("main:app", port=config("PORT", cast=int), reload=True)
