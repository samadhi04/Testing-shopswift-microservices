from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from schemas import Product, ProductCreate, ProductUpdate
from crud import (
    get_all_products,
    get_product,
    get_product_by_sku,
    create_product,
    delete_product, 
    update_product,)
from typing import List

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Product Service", version="1.0")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Product Service is running"}

@app.get("/api/products", response_model=List[Product])
def get_products(db: Session = Depends(get_db)):
    return get_all_products(db)

@app.get("/api/products/{product_id}", response_model=Product)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/api/products", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product_endpoint(product: ProductCreate, db: Session = Depends(get_db)):
    existing = get_product_by_sku(db, product.sku)
    if existing:
        raise HTTPException(status_code=400, detail="SKU already exists")
    return create_product(db, product)

@app.put("/api/products/{product_id}", response_model=Product)
def update_product_endpoint(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    updated = update_product(db, product_id, product)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

@app.delete("/api/products/{product_id}")
def delete_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    success = delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted"}