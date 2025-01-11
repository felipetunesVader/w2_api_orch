from fastapi import APIRouter, File, UploadFile
from app.services.plate_service import get_plate_number_service, process_full_car_service

router = APIRouter()

@router.post("/get-plate-number")
async def get_plate_number(files: list[UploadFile] = File(...)):
    """
    Recebe múltiplas imagens e retorna os caracteres das placas detectadas.
    """
    results = {}
    for file in files:
        try:
            plate_number = get_plate_number_service(file)
            results[file.filename] = plate_number
        except Exception as e:
            results[file.filename] = f"Erro ao processar: {str(e)}"
    return results


@router.post("/process-full-car")
async def process_full_car(file: UploadFile = File(...)):
    """
    Processa uma imagem de carro completo, detecta a placa, faz o zoom e lê os caracteres.
    """
    try:
        result = process_full_car_service(file)
        return result
    except Exception as e:
        return {"error": str(e)}
