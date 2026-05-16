import base64
from pathlib import Path
from django.http import JsonResponse
from PIL import Image
from io import BytesIO
from django.shortcuts import render
from django.http import HttpResponse
from backend.generate_result import process_image
from backend.infrastructure.google_ocr.ocr import GoogleOCR

BASE_DIR = Path(__file__).resolve().parent.parent
json_path = BASE_DIR / "backend" / "ocr_api_key.json"

ocr_service = GoogleOCR(json_path)
def home(request):
    return render(request, "home.html")

def upload_image(request):
    if request.method == "POST":
        img = request.FILES["image"]
        background_file = request.FILES.get('background')
        if background_file:
            background_image = Image.open(background_file).convert("RGBA")
        else:
            background_image = None
    
        image = Image.open(img)  # ✔ 直接用檔案物件
        print(image.size)
        result = process_image(source = image, ocr_service = ocr_service, background_image = background_image)
        output_image = result["image"]
        img_base64 = img_to_b64(output_image)

        return JsonResponse({
            "status": "success",
            "data": {
                "image": {
                    "base64": img_base64,
                    "format": "png"
                },
                "result": result["result"],
            }
        })

    return HttpResponse("只接受 POST")

def img_to_b64(image):
    buf = BytesIO()
    image.save(buf, format="PNG")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    return img_base64
