import easyocr
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image
from generate_result import process_image_in_memory
from io import BytesIO

app = Flask(__name__)
CORS(app)

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

    # return jsonify({
    #     "text": result.get("text", ""),
    #     "image_base64": result["image_base64"],  
    # })
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

if __name__ == "__main__":
    app.run(
        host = "0.0.0.0",
        port = 5000,
        debug = True
    )