import os
import easyocr
from flask import Flask, request, jsonify, send_file, send_from_directory
from PIL import Image
from generate_result import process_image_in_memory
from io import BytesIO

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
FRONTEND_DIST = os.path.join(BASE_DIR, "..", "frontend", "dist")
app = Flask(
     __name__, 
     static_folder=FRONTEND_DIST,
    static_url_path="/" 
) 

ocr_reader = easyocr.Reader(['en', 'ch_tra'])  

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

    result =  process_image_in_memory(image, ocr_reader)

    output_image = result["image"]
    buf = BytesIO()
    output_image.save(buf, format = "PNG")
    buf.seek(0)

    return send_file(
        buf,
        mimetype = "image/png",
        as_attachment = False,
        download_name = "result.png",
    )

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    full_path = os.path.join(app.static_folder, path)
    if path and os.path.exists(full_path):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(
        host = "0.0.0.0",
        port = 3000,
        debug = True
    )