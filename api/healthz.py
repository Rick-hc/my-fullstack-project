# api/healthz.py
from fastapi import FastAPI
from mangum import Mangum   # ★ ここが必須

app = FastAPI()

@app.get("/")
def healthz():
    return {"status": "ok"}

handler = Mangum(app)       # ★ Vercel が検出するエクスポート
