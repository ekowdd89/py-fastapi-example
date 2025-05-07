from fastapi import FastAPI, Query, Path

from typing import Annotated

app = FastAPI()


from models.base_model import FilterParam, Item

fake_items_db = [{"item_id": i, "name": f"Item {i}"} for i in range(1000)]

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/items")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


@app.get("/users")
async def read_users():
    return [
        {"username": "eko", "full_name": "Eko Widodo", "email": "eko@example.com"},
        {"username": "john", "full_name": "John Doe", "email": "john@example.com"}
    ]

@app.post("/items")
async def create_item(item: Item):
    item_dict = item.model_dump() # deprecated item.dict() use item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result

@app.get("/itms/")

# tanpa annotated q: str | None = Query(default=None, min_length=3, max_length=10)
# dengan annotated q: Annotated[str, Query(min_length=3, max_length=10)] = "eko"
# tanpa annotated q: str  = Query(default="eko", min_length=3, max_length=9)
async def read_itms(q: str = Query(default="eko", min_length=3, max_length=9)):
    results = {"items": [{"item_id": i} for i in range(1000)]}
    if q:
        results.update({"q": q})
    return results


#example path

# Annotated validate ge=1 (greater than or equal to 1) or >=1  ===>  Annotated[int , Path("test",ge=1)]
# Annotated validate gt=1 (greater than 1) or >1 le (less than or equal to) or <=1 ====>  Annotated[int , Path("test",gt=1,le=1)]
# Anotated[float, Query(gt=1,lt=1)] gt = greater than lt = less than / or >1 <1


"""
Keterangan
gt = greater than ==> atau >
ge = greater than or equal to ==> atau >=
lt = less than ==> atau <
lt = less than ==> atau <=
le = less than or equal to ==> atau <=

"""

@app.get("/pthexample/{item_id}")
async def read_items_example(
    item_id: Annotated[int, Path(title="Item ID")],
    q: Annotated[str, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@app.get("/filterParam")
async def read_items_filterParam(
    filter_query: Annotated[FilterParam, Query()]
):
    return filter_query