from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import httpx
from typing import Any

app = FastAPI(title="ShopSwift API Gateway", version="1.0")

SERVICES = {
    "user": "http://localhost:8001",
    "product": "http://localhost:8002",
    "cart": "http://localhost:8003",
    "order": "http://localhost:8004",
    "notification": "http://localhost:8005"
}

async def forward_request(service: str, path: str, method: str, **kwargs) -> Any:
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail="Service not found")
    url = f"{SERVICES[service]}{path}"
    async with httpx.AsyncClient() as client:
        try:
            if method == "GET":
                response = await client.get(url, **kwargs)
            elif method == "POST":
                response = await client.post(url, **kwargs)
            elif method == "PUT":
                response = await client.put(url, **kwargs)
            elif method == "DELETE":
                response = await client.delete(url, **kwargs)
            else:
                raise HTTPException(status_code=405, detail="Method not allowed")
            return JSONResponse(
                content=response.json() if response.text else None,
                status_code=response.status_code
            )
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "ShopSwift API Gateway is running", "services": list(SERVICES.keys())}

# User Service Routes
@app.get("/gateway/users")
async def get_all_users():
    return await forward_request("user", "/api/users", "GET")

@app.get("/gateway/users/{user_id}")
async def get_user_by_id(user_id: int):
    return await forward_request("user", f"/api/users/{user_id}", "GET")

@app.post("/gateway/users")
async def create_user(request: Request):
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")
    return await forward_request("user", "/api/users", "POST", json=payload)

@app.put("/gateway/users/{user_id}")
async def update_user(user_id: int, request: Request):
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")
    return await forward_request("user", f"/api/users/{user_id}", "PUT", json=payload)

@app.delete("/gateway/users/{user_id}")
async def delete_user(user_id: int):
    return await forward_request("user", f"/api/users/{user_id}", "DELETE")

# Product Service Routes
@app.get("/gateway/products")
async def get_all_products():
    return await forward_request("product", "/api/products", "GET")

@app.get("/gateway/products/{product_id}")
async def get_product_by_id(product_id: int):
    return await forward_request("product", f"/api/products/{product_id}", "GET")

@app.post("/gateway/products")
async def create_product(request: Request):
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")
    return await forward_request("product", "/api/products", "POST", json=payload)

@app.put("/gateway/products/{product_id}")
async def update_product(product_id: int, request: Request):
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")
    return await forward_request("product", f"/api/products/{product_id}", "PUT", json=payload)

@app.delete("/gateway/products/{product_id}")
async def delete_product(product_id: int):
    return await forward_request("product", f"/api/products/{product_id}", "DELETE")

# Cart Service Routes
@app.get("/gateway/cart/{user_id}")
async def get_user_cart(user_id: int):
    return await forward_request("cart", f"/api/cart/{user_id}", "GET")

@app.get("/gateway/cart")
async def get_user_cart_by_query(user_id: int):
    return await forward_request("cart", f"/api/cart/{user_id}", "GET")

@app.post("/gateway/cart")
async def add_item_to_cart(request: Request):
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")
    return await forward_request("cart", "/api/cart", "POST", json=payload)

@app.delete("/gateway/cart/{item_id}")
async def remove_item_from_cart(item_id: int):
    return await forward_request("cart", f"/api/cart/{item_id}", "DELETE")
