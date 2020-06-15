import pydantic


class Item(pydantic.BaseModel):
    name: str
    price: float
