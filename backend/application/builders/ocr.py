from render.layout_config import OCR_CROP_AREAS
from infrastructure.ocr.google_ocr import GoogleOCR

def run_ocr(source):
    engine = GoogleOCR("config.json")
    return engine.ocr(source, OCR_CROP_AREAS)
