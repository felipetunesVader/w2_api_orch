from ultralytics import YOLO
from PIL import Image
import cv2
import numpy as np
from fastapi import UploadFile

# Caminho completo do modelo YOLOv8 treinado
MODEL_PATH = '/Users/W10/Desktop/w2_api_orch/w2_api/app/utils/best_pre.pt'

model = YOLO(MODEL_PATH)  # Carregar o modelo

def get_plate_number_service(file: UploadFile) -> str:
    """
    Processa a imagem carregada e extrai os caracteres da placa.
    """
    try:
        # Carregar a imagem do upload
        file_bytes = np.asarray(bytearray(file.file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # Fazer a inferência na imagem
        results = model(image)
        result = results[0]

        # Extrair caracteres detectados
        detected_characters = []
        for box in result.boxes:
            x1 = int(box.xyxy[0][0])
            class_id = int(box.cls[0].item())
            character = model.names[class_id]
            detected_characters.append((x1, character))

        # Ordenar os caracteres da esquerda para a direita
        detected_characters = sorted(detected_characters, key=lambda x: x[0])
        plate_text = ''.join([char for _, char in detected_characters])

        return plate_text

    except Exception as e:
        raise RuntimeError(f"Erro ao processar a imagem: {e}")
