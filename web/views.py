import base64
from pathlib import Path
from django.http import JsonResponse
from PIL import Image
from io import BytesIO
from django.shortcuts import render
from django.http import HttpResponse
from backend.generate_result import process_image
from backend.infrastructure.google_ocr.ocr import GoogleOCR

from history.models import EchoHistory
from django.core.files.base import ContentFile
import uuid
from django.db.models import Count

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
        result = process_image(source = image, ocr_service = ocr_service, background_image = background_image)
        output_image = result["image"]

        img_base64 = img_to_b64(output_image)
        # 儲存結果圖
        result_file = pil_to_file(output_image)
        # 原圖重新讀取
        img.seek(0)
        
        EchoHistory.objects.create(
            user=request.user,
            image=result_file
        )
        enforce_limit(request.user)
        
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

def pil_to_file(image):
    
    # 建立記憶體 buffer
    buffer = BytesIO()

    # 把 PIL Image 存進 buffer
    image.save(buffer, format="PNG")

    # buffer.getvalue() 會拿到 binary bytes
    image_bytes = buffer.getvalue()

    # Django File object
    return ContentFile(
        image_bytes,
        name=f"{uuid.uuid4()}.png"
    )

def enforce_limit(user):
    qs = EchoHistory.objects.filter(user=user).order_by("-created_at")

    if qs.count() > 5:
        # 刪最舊的
        for item in qs[5:]:
            item.delete()