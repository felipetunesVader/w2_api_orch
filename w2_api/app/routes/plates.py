from fastapi import APIRouter, File, UploadFile
from app.services.plate_service import get_plate_number_service

router = APIRouter()

@router.post("/get-plate-number")
async def get_plate_number(file: UploadFile = File(...)):
    """
    Recebe uma imagem e retorna os caracteres da placa.
    """
    try:
        plate_number = get_plate_number_service(file)
        return {"plate_number": plate_number}
    except Exception as e:
        return {"error": str(e)}
