from render.layout.config import OCR_CROP_AREAS

def run_ocr(service, source):
    return service.recognize(source, OCR_CROP_AREAS)