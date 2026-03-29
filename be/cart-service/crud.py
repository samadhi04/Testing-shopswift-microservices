from sqlalchemy.orm import Session
from models import CartItem
from schemas import CartItemCreate

def get_cart_by_user(db: Session, user_id: int):
    return db.query(CartItem).filter(CartItem.user_id == user_id).all()

def get_cart_item_by_user_product(db: Session, user_id: int, product_id: int):
    return db.query(CartItem).filter(
        CartItem.user_id == user_id,
        CartItem.product_id == product_id
    ).first()

def add_to_cart(db: Session, cart_item: CartItemCreate):
    db_item = CartItem(**cart_item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def remove_from_cart(db: Session, item_id: int):
    db_item = db.query(CartItem).filter(CartItem.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False