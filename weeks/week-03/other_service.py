from fastapi import FastAPI

app = FastAPI(title="ДОПОЛНИТЕЛЬНЫЙ СЕРВИС")

@app.get("/")
@app.get("/{path:path}")
async def catch_all(path: str = ""):
    return {"message": "Это доп. сервис для теста", "path": path, "service": "other"}

@app.post("/")
@app.post("/{path:path}")
async def catch_all_post(path: str = ""):
    return {"message": "Это доп. сервис для теста", "path": path, "service": "other"}