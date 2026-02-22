from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import List
from schemas import Invoice, InvoiceCreate

app = FastAPI(title="invoices")

invoices_db = []
id_counter = 1

@app.exception_handler(Exception)
async def handle_all_errors(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Ошибка сервера"})

@app.post("/api/invoices/", response_model=Invoice, status_code=201,responses={
              201: {"description":"Инвойс успешно создан"},
              400: {"description":"Неверные данные"},
              422: {"description":"Ошибка валидации данных"},
              500: {"description":"Ошибка сервера"}})
async def create_invoice(invoice: InvoiceCreate):
    global id_counter
    new_invoice = Invoice(id=id_counter, **invoice.model_dump())
    invoices_db.append(new_invoice)
    id_counter += 1
    return new_invoice

@app.get("/api/invoices/", response_model=List[Invoice],responses={
             200: {"description":"Список инвойсов успешно получен"},
             204: {"description":"Нет инвойсов"},
             500: {"description":"Ошибка сервера"}})
async def get_invoices():
    return invoices_db

@app.get("/api/invoices/{invoice_id}", response_model=Invoice,responses={
             200: {"description":"Инвойс успешно получен"},
             204: {"description":"Нет инвойса"},
             500: {"description":"Ошибка сервера"}})
async def get_invoice(invoice_id: int):
    invoice = next((p for p in invoices_db if p.id == invoice_id), None)
    if not invoice:
        raise HTTPException(status_code=404, detail="Инвойс не найден")
    return invoice

@app.put("/api/invoices/{invoice_id}",response_model=Invoice,responses={
    200: {"description":"Инвойс успешно обновлен"},
    404: {"description":"Инвойс не найден"},
    400: {"description":"Неверные данные"},
    422: {"description":"Ошибка валидации данных"},
    500: {"description":"Ошибка сервера"}})
async def update_invoice(invoice_id: int, invoice: InvoiceCreate):
    for i, p in enumerate(invoices_db):
        if p.id == invoice_id:
            updated_invoice = Invoice(id=invoice_id, **invoice.model_dump())
            invoices_db[i] = updated_invoice
            return updated_invoice
    raise HTTPException(status_code=404, detail="Инвойс не найден")

@app.delete("/api/invoices/{invoice_id}",status_code=204,responses={
    204: {"description":"Инвойс успешно удален"},
    404: {"description":"Инвойс не найден"},
    500: {"description":"Ошибка сервера"}})
async def delete_invoice(invoice_id: int):
    global invoices_db
    for i, p in enumerate(invoices_db):
        if p.id == invoice_id:
            invoices_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="Инвойс не найден")