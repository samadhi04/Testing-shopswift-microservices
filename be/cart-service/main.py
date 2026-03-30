from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from schemas import CartItem, CartItemCreate
from crud import (
    get_cart_by_user,
    add_to_cart,
    remove_from_cart,
    get_cart_item_by_user_product,
)
import httpx
from typing import List

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cart Service", version="1.0")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Cart Service is running"}

@app.get("/api/cart/{user_id}", response_model=List[CartItem])
def get_user_cart(user_id: int, db: Session = Depends(get_db)):
    return get_cart_by_user(db, user_id)

@app.post("/api/cart", response_model=CartItem, status_code=status.HTTP_201_CREATED)
def add_item_to_cart(cart_item: CartItemCreate, db: Session = Depends(get_db)):
    # Inter-service call: check if user exists
    with httpx.Client() as client:
        user_resp = client.get(f"http://localhost:8001/api/users/{cart_item.user_id}")
        if user_resp.status_code != 200:
            raise HTTPException(status_code=404, detail="User not found")
        # Check if product exists
        product_resp = client.get(f"http://localhost:8002/api/products/{cart_item.product_id}")
        if product_resp.status_code != 200:
            raise HTTPException(status_code=404, detail="Product not found")
    # Check if item already in cart for this user
    existing = get_cart_item_by_user_product(db, cart_item.user_id, cart_item.product_id)
    if existing:
        raise HTTPException(status_code=400, detail="Product already in cart")
    return add_to_cart(db, cart_item)

@app.delete("/api/cart/{item_id}")
def remove_item_from_cart(item_id: int, db: Session = Depends(get_db)):
    success = remove_from_cart(db, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return {"message": "Item removed from cart"}