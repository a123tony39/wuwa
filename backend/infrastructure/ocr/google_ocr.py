import io
import re
import json
from PIL import Image
from google.cloud import vision
from dataclasses import dataclass

@dataclass
class OCRResult:
    player_block: list[str]
    echo_block: list[str]

class GoogleOCR:
    def __init__(self, api_key_file = "config.json"):
        with open(api_key_file, "r") as f:
            config = json.load(f)
        self.api_key = config["GOOGLE_VISION_API_KEY"]
        self.client = vision.ImageAnnotatorClient(
            client_options={"api_key": self.api_key}
        )
    
    def preprocess_image(self, img, crop_areas, scale=2):
        """
        將每個 crop area 切出放大後，貼回新圖
        scale: 放大倍數
        """
        # 計算新圖大小
        new_width = sum(int((x2 - x1) * scale) for x1, y1, x2, y2 in crop_areas)
        new_height = max(int((y2 - y1) * scale) for x1, y1, x2, y2 in crop_areas)

        new_img = Image.new("RGB", (new_width, new_height), color=(255, 255, 255))

        current_x = 0
        for x1, y1, x2, y2 in crop_areas:
            crop = img.crop((x1, y1, x2, y2))
            w, h = crop.size
            crop = crop.resize((int(w * scale), int(h * scale)), Image.BICUBIC)
            new_img.paste(crop, (current_x, 0))
            current_x += crop.width

        return new_img
        
    def ocr(self, img, crop_areas, scale=2):
        # 先處理圖像
        img_proc = self.preprocess_image(img, crop_areas, scale=scale)

        with open("config.json", "r") as f:
            config = json.load(f)
        api_key = config["GOOGLE_VISION_API_KEY"]
        client = vision.ImageAnnotatorClient(
            client_options={"api_key": api_key}
        )

        buf = io.BytesIO()
        img_proc.save(buf, format="PNG")
        content = buf.getvalue()
        img_vision = vision.Image(content=content)

        response = client.text_detection(image=img_vision)
        texts = response.text_annotations

        # texts[0] 是整張文字，其餘是每個字或區塊
        all_text_per_area = [[] for _ in crop_areas]

        # 計算每個 crop 在新圖中的水平起始 x
        area_x_starts = []
        current_x = 0
        for x1, y1, x2, y2 in crop_areas:
            area_x_starts.append(current_x)
            current_x += int((x2 - x1) * scale)

        for text in texts[1:]:  
            vertices = text.bounding_poly.vertices
            min_x = min(v.x for v in vertices)
            max_x = max(v.x for v in vertices)
            min_y = min(v.y for v in vertices)
            max_y = max(v.y for v in vertices)

            for i, (x1, y1, x2, y2) in enumerate(crop_areas):
                area_start_x = area_x_starts[i]
                area_end_x = area_start_x + int((x2 - x1) * scale)
                # 判斷文字是否在 crop 區域
                if min_x >= area_start_x and max_x <= area_end_x:
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

        # 合併文字成行
        result = []
        for items in all_text_per_area:
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

        return OCRResult(
            player_block = result[0],
            echo_block = result[1:]
        )