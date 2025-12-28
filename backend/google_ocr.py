import io
import re
import json
from google.cloud import vision
from PIL import Image


def google_ocr(img):
    # ----------------------------
    # 1️⃣ 設定裁切區域 (x1, y1, x2, y2)
    crop_areas = [
        (0, 0, 300, 150),
        (60, 710, 380, 1050),
        (440, 710, 380*2, 1050),
        (815, 710, 380*3, 1050),
        (1190, 710, 380*4, 1050),
        (1560, 710, 380*5, 1050),
    ]
    # 3️⃣ 初始化 Google Vision API
    with open("config.json", "r") as f:
        config = json.load(f)
    api_key = config["GOOGLE_VISION_API_KEY"]
    client = vision.ImageAnnotatorClient(
        client_options={"api_key": api_key}
    )

    # 4️⃣ 送整張圖片做 OCR
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    content = buf.getvalue()

    img = vision.Image(content=content)
    response = client.text_detection(image=img)
    texts = response.text_annotations

    # 5️⃣ 處理文字區塊
    # texts[0] 是整張文字描述，其餘是每個文字或區塊
    all_text_per_area = [[] for _ in crop_areas]

    result = []
    for text in texts[1:]:  # 忽略第一筆整張文字
        # bounding box 座標
        vertices = text.bounding_poly.vertices
        min_x = min(v.x for v in vertices)
        max_x = max(v.x for v in vertices)
        min_y = min(v.y for v in vertices)
        max_y = max(v.y for v in vertices)

        # 判斷文字所在區域
        for i, (x1, y1, x2, y2) in enumerate(crop_areas):
            if min_x >= x1 and max_x <= x2 and min_y >= y1 and max_y <= y2:
                # 過濾 ICON / 奇怪符號
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
                break  # 一個文字只屬於一個區域

    # 6️⃣ 輸出每個區域文字
    for i, items in enumerate(all_text_per_area):
        # 依 y 排序（由上到下）
        items.sort(key=lambda x: (x["y"], x["x"]))

        lines = []
        current_line = []
        last_y = None

        for item in items:
            if last_y is None or abs(item["y"] - last_y) < 15:
                # 同一行 → 接起來
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