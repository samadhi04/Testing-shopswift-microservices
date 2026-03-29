from pydantic import BaseModel
from typing import Optional

class CartItemBase(BaseModel):
    user_id: int
    product_id: int
    quantity: int

class CartItemCreate(CartItemBase):
    pass

class CartItem(CartItemBase):
    id: int
    class Config:
        from_attributes = True