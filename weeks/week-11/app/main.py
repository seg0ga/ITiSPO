from fastapi import FastAPI, HTTPException,Request
from typing import List
from schemas import Product, ProductCreate
from fastapi.responses import JSONResponse

app = FastAPI(title="Inventory Microservice")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Имитация базы данных в памяти
products_db = []
id_counter = 1

@app.exception_handler(Exception)
async def handle_all_errors(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Ошибка сервера"}
    )

@app.post("/products/", response_model=Product, status_code=201,responses={
              201: {"description":"Товар успешно создан"},
              400: {"description":"Неверные данные"},
              422: {"description":"Ошибка валидации данных"},
              500: {"description":"Ошибка сервера"}})
async def create_product(product: ProductCreate):
    global id_counter
    new_product = Product(id=id_counter, **product.model_dump())
    products_db.append(new_product)
    id_counter += 1
    return new_product

@app.get("/products/", response_model=List[Product],responses={
             200: {"description":"Список товаров успешно получен"},
             204: {"description":"Нет товаров"},
             500: {"description":"Ошибка сервера"}})
async def get_products():
    return products_db

@app.get("/products/{product_id}", response_model=Product,responses={
             200: {"description":"Товар успешно получен"},
             204: {"description":"Нет товара"},
             500: {"description":"Ошибка сервера"}})
async def get_product(product_id: int):
    product = next((p for p in products_db if p.id == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product

@app.put("/products/{product_id}",response_model=Product,responses={
    200: {"description":"Товар успешно обновлен"},
    404: {"description":"Товар не найден"},
    400: {"description":"Неверные данные"},
    422: {"description":"Ошибка валидации данных"},
    500: {"description":"Ошибка сервера"}
})
async def update_product(product_id: int, product: ProductCreate):
    for i, p in enumerate(products_db):
        if p.id == product_id:
            updated_product = Product(id=product_id, **product.model_dump())
            products_db[i] = updated_product
            return updated_product
    raise HTTPException(status_code=404, detail="Товар не найден")

@app.delete("/products/{product_id}",status_code=204,responses={
    204: {"description":"Товар успешно удален"},
    404: {"description":"Товар не найден"},
    500: {"description":"Ошибка сервера"}})
async def delete_product(product_id: int):
    global products_db
    for i, p in enumerate(products_db):
        if p.id == product_id:
            products_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="Товар не найден")