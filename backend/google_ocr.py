import io
import re
import json
from google.cloud import vision
from PIL import Image

def google_ocr(img, crop_areas):
    with open("config.json", "r") as f:
        config = json.load(f)
    api_key = config["GOOGLE_VISION_API_KEY"]
    client = vision.ImageAnnotatorClient(
        client_options={"api_key": api_key}
    )

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    content = buf.getvalue()

    img = vision.Image(content=content)
    response = client.text_detection(image=img)
    texts = response.text_annotations

    # texts[0] 是整張文字描述，其餘是每個文字或區塊
    all_text_per_area = [[] for _ in crop_areas]

    result = []
    for text in texts[1:]:  
        # bounding box
        vertices = text.bounding_poly.vertices
        min_x = min(v.x for v in vertices)
        max_x = max(v.x for v in vertices)
        min_y = min(v.y for v in vertices)
        max_y = max(v.y for v in vertices)

        for i, (x1, y1, x2, y2) in enumerate(crop_areas):
            if min_x >= x1 and max_x <= x2 and min_y >= y1 and max_y <= y2:
                if i == 0:
                    filtered_text = re.sub(r"[^0-9a-zA-Z\u4e00-\u9fff\s:.\%]", "", text.description)
                else:
                    filtered_text = re.sub(r"[^0-9\u4e00-\u9fff\s:.\%]", "", text.description)
                filtered_text = filtered_text.strip()
                if filtered_text:
                    all_text_per_area[i].append({
                        "x": min_x,
                        "y": min_y,
                        "text": filtered_text
                    })
                break  

    for i, items in enumerate(all_text_per_area):
        items.sort(key=lambda x: (x["y"], x["x"]))

        lines = []
        current_line = []
        last_y = None

        for item in items:
            if last_y is None or abs(item["y"] - last_y) < 15:
                current_line.append(item)
            else:
                lines.append(current_line)
                current_line = [item]
            last_y = item["y"]

        if current_line:
            lines.append(current_line)

        block = []
        for line_items in lines:
            line_items.sort(key=lambda x: x["x"])
            text = "".join(x["text"] for x in line_items)
            block.append(text)
        result.append(block)
      
    return result

if __name__ == "__main__":
    img = Image.open("../img/input/Zani.png")
    results = google_ocr(img)
    for result in results:
        print(result)
        print("-----")