from fastapi import FastAPI

from app.routers import (
    auth,
    users,
    categories,
    products,
    cart,
    orders,
    payments,
    addresses,
)


app = FastAPI(
    title="E-Commerce Backend API",
    version="1.0.0",
)


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(payments.router)
app.include_router(addresses.router)


@app.get("/")
def root():
    return {
        "message": "E-Commerce Backend API is running"
    }