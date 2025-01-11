from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Importe o CORS Middleware
from app.routes import plates

app = FastAPI(title="Plate Recognition API", version="1.0")

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite requisições de qualquer origem (ajuste em produção)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os headers
)

# Register routes
app.include_router(plates.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Plate Recognition API!"}
