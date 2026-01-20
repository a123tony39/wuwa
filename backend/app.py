import os
import base64
from PIL import Image
from io import BytesIO
from flask import Flask, request, jsonify, send_from_directory
from generate_result import process_image
from infrastructure.google_ocr.ocr import GoogleOCR

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
FRONTEND_DIST = os.path.join(BASE_DIR, "..", "frontend", "dist")
ocr_service = GoogleOCR("config.json")
app = Flask(
    __name__, 
    static_folder=FRONTEND_DIST,
    static_url_path="/" 
) 


@app.route("/api/health", methods =["GET"])
def health_check():
    return jsonify({
        "status": "ok",
        "message": "API is running"
    })

@app.route("/api/process", methods = ["POST"])
def analysis_echo():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    
    image = Image.open(file.stream)
    background_file = request.files.get('background')
    if background_file:
        background_image = Image.open(background_file.stream).convert("RGBA")
    else:
        background_image = None
    result = process_image(source = image, ocr_service = ocr_service, background_image=background_image)
    output_image = result["image"]
    img_base64 = img_to_b64(output_image)
    return jsonify({
        "message": "圖片處理完成",
        "image_base64": f"{img_base64}",
        "result": result['result'],
    })

@app.route("/", defaults={"path": ""})
@app.route("/<string:path>")
@app.route("/<path:path>")
def serve_frontend(path):
    full_path = os.path.join(app.static_folder, path)
    if path and os.path.exists(full_path):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")

def img_to_b64(image):
    buf = BytesIO()
    image.save(buf, format="PNG")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    return img_base64

if __name__ == "__main__":
    app.run(
        host = "0.0.0.0",
        port = int(os.environ.get("PORT", 5000)),
        debug = True
    )