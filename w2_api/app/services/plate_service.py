from ultralytics import YOLO
from PIL import Image
import cv2
import numpy as np
from fastapi import UploadFile
import os

# Caminho do modelo YOLOv8 treinado para reconhecimento de caracteres
MODEL_PATH = '/Users/W10/Desktop/w2_api_orch/w2_api/app/utils/best_pre.pt'
model = YOLO(MODEL_PATH)  # Carregar o modelo de reconhecimento de placas

# Caminho do Haar Cascade para detecção de placas
PLATE_CASCADE_PATH = '/Users/W10/Desktop/w2_api_orch/w2_api/app/utils/haarcascade_russian_plate_number.xml'
if not os.path.exists(PLATE_CASCADE_PATH):
    raise FileNotFoundError(f"Haar Cascade file not found at {PLATE_CASCADE_PATH}")
plate_cascade = cv2.CascadeClassifier(PLATE_CASCADE_PATH)


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


def process_full_car_service(file: UploadFile) -> dict:
    """
    Processa uma imagem de carro completo, detecta a placa, faz o zoom e lê os caracteres.
    """
    try:
        # Carregar a imagem
        file_bytes = np.asarray(bytearray(file.file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # Converter para escala de cinza para usar Haar Cascade
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        plates = plate_cascade.detectMultiScale(
            gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )

        if len(plates) == 0:
            raise RuntimeError("Placa não encontrada na imagem.")

        # Para simplificar, processaremos apenas a primeira placa detectada
        x, y, w, h = plates[0]

        # Fazer o "zoom" na região da placa
        plate_roi = image[y:y + h, x:x + w]

        # Inferência com YOLO para reconhecimento dos caracteres da placa
        results = model(plate_roi)
        result = results[0]

        detected_characters = []
        for box in result.boxes:
            x1 = int(box.xyxy[0][0])
            class_id = int(box.cls[0].item())
            character = model.names[class_id]
            detected_characters.append((x1, character))

        # Ordenar os caracteres da esquerda para a direita
        detected_characters = sorted(detected_characters, key=lambda x: x[0])
        plate_text = ''.join([char for _, char in detected_characters])

        return {
            "plate_coordinates": {"x": int(x), "y": int(y), "width": int(w), "height": int(h)},
            "plate_text": plate_text,
        }

    except Exception as e:
        raise RuntimeError(f"Erro ao processar a imagem do carro: {e}")
