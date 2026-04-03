import os
import base64
import logging
from PIL import Image
from io import BytesIO
from flask import Flask, request, jsonify, send_from_directory
from generate_result import process_image
from infrastructure.google_ocr.ocr import GoogleOCR

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
FRONTEND_DIST = os.path.join(BASE_DIR, "..", "frontend", "dist")
ocr_service = GoogleOCR("ocr_api_key.json")
app = Flask(
    __name__, 
    static_folder=FRONTEND_DIST,
    static_url_path="/" 
) 

file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s'
)
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)


@app.route("/api/health", methods =["GET"])
def health_check():
    app.logger.info("Health check endpoint called")
    return jsonify({
        "status": "ok",
        "message": "API is running"
    })

@app.route("/api/process", methods = ["POST"])
def analysis_echo():
    app.logger.info("Process endpoint called")
    if 'file' not in request.files:
        app.logger.warning("No file upload")
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    app.logger.info(f"Uploaded file: {file.filename}, Content-Type: {file.content_type}")
    
    image = Image.open(file.stream)
    background_file = request.files.get('background')
    if background_file:
        background_image = Image.open(background_file.stream).convert("RGBA")
        app.logger.info(f"background_file uploaded: {background_file.filename}")
    else:
        background_image = None
        app.logger.info("No background file uploaded, use default background")

    app.logger.info("Start image processing...")
    result = process_image(source = image, ocr_service = ocr_service, background_image=background_image)
    output_image = result["image"]
    img_base64 = img_to_b64(output_image)
    
    app.logger.info("Returning response with base64 image")
    return jsonify({
        "message": "圖片處理完成",
        "image_base64": f"{img_base64}",
        "result": result['result'],
    })

@app.route("/", defaults={"path": ""})
@app.route("/<string:path>")
@app.route("/<path:path>")
def serve_frontend(path):
    if path == "":
        app.logger.info("A viewer visited")
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