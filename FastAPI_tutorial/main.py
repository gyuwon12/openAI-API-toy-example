"""
FastAPI Tutorial Code.
"""

from fastapi import FastAPI # API import
from typing import Optional # optional condition
from pydantic import BaseModel 

app = FastAPI() # class instance화

"""
CRUD : Create, Read, Update, Delete

app.get : read
app.post : create
app.put : update
app.delete : delete
"""

items = {
    0: {"name": "bread", "price": 1000},
    1: {"name": "water", "price": 500},
    2: {"name": "라면", "price": 1200},
}

# Path parameter -> 기본적으로 string
@app.get("/items/{item_id}") # 데코레이터
def read_item(item_id: int): # 기본적으로 paramter가 string으로 인식이 되니 integer change 필요
    item = items[item_id]
    return item

@app.get("/items/{item_id}/{key}")
def read_item_and_key(item_id: int, key: str): # 기본적으로 paramter가 string으로 인식이 되니 integer change 필요
    item = items[item_id][key]
    return item

# Query parameter -> '?'를 사용
@app.get("/item-by-name")
def read_item_by_name(name: str):
    for item_id, item in items.items(): # dic 순회하는 방법 items() method
        if item['name'] == name:
            return item
    return {"error": "data not found"}

class Item(BaseModel):
    name: str
    price: int

# Create
@app.post("/items/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in items: # 덮어쓰기 방지
        return {"error": "there is already key"}
    items[item_id] = item.dict() # 형변환
    return {"success": "ok"}

class ItemForUpdate(BaseModel): # 그냥 Item class를 쓰면, 선택적 정보 업데이트가 안돼
    name: Optional[str]
    price: Optional[int]

# Update
@app.put("/items/{item_id}")
def update_item(item_id: int, item: ItemForUpdate):
    if item_id not in items:
       return {"error": f"there is no item id: {item_id}"}
    
    if item.name:
        items[item_id]['name'] = item.name
        
    if item.price:
        items[item_id]['price'] = item.price
        
    return {"success": "ok"}

# Delete
@app.delete("/itmes/{item_id}")
def delete_item(item_id: int):
    items.pop(item_id)
    return {"success": "ok"}