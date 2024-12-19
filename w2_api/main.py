from fastapi import FastAPI
from app.routes import plates

app = FastAPI(title="Plate Recognition API", version="1.0")

# Register routes
app.include_router(plates.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Plate Recognition API!"}
