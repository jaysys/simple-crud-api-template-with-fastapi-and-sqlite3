#simple api server built with python fastapi

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="CRUD API with FastAPI and SQLite",
    description="simple CRUD API built with FastAPI and SQLite3.",
    version="1.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# SQLite3 데이터베이스 연결
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# 테이블 생성
cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY,
        name TEXT,
        price REAL
    )
""")
conn.commit()


# 모델 정의
class Item(BaseModel):
    name: str
    price: float


# 아이템 생성
@app.post("/items/", summary="Create Item", tags=["Items"])
async def create_item(item: Item):
    """
    Create a new item.
    """
    cursor.execute("INSERT INTO items (name, price) VALUES (?, ?)", (item.name, item.price))
    conn.commit()
    print({"message": "Item created successfully"})    
    return {"message": "Item created successfully"}


# 아이템 조회
@app.get("/items/{item_id}", summary="Read Item", tags=["Items"])
async def read_item(item_id: int):
    """
    Read details of a specific item.
    """
    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    item = cursor.fetchone()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    print ({"id": item[0], "name": item[1], "price": item[2]})
    return {"id": item[0], "name": item[1], "price": item[2]}


# 아이템 업데이트
@app.put("/items/{item_id}", summary="Update Item", tags=["Items"])
async def update_item(item_id: int, item: Item):
    """
    Update details of a specific item.
    """
    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    existing_item = cursor.fetchone()
    if existing_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    try:
        cursor.execute("UPDATE items SET name = ?, price = ? WHERE id = ?", (item.name, item.price, item_id))
        conn.commit()
        print ({"message": "Item updated successfully"})
        return {"message": "Item updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


# 아이템 삭제
@app.delete("/items/{item_id}", summary="Delete Item", tags=["Items"])
async def delete_item(item_id: int):
    """
    Delete a specific item.
    """
    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    existing_item = cursor.fetchone()
    if existing_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    try:
        cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
        conn.commit()
        print ({"message": "Item deleted successfully"})
        return {"message": "Item deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
