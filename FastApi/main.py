from fastapi import FastAPI

app = FastAPI()

@app.post("/packages")
def create_package(data: dict):
    print("📥 Paquete recibido en API")
    return {"status": "ok"}