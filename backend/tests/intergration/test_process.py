import pytest
from unittest.mock import patch, MagicMock
from generate_result import process_image
from PIL import Image

class FakeOCRResults:
    def __init__(self):
        self.player_block = ["弗洛洛", "LV.90", "玩家名稱:Testuser01", "特徵碼:800634045"]
        self.echo_block = [
            ["暴擊傷害", "44%", "攻擊150", "暴擊10.5%", "攻擊8.6%", "暴擊傷害19.8%", "攻擊50", "防禦60"],
            ["湮滅傷害加成", "30%", "攻擊100", "暴擊傷害18.6%", "生命320", "共鳴技能傷害加成7.9%", "攻擊60", "暴擊7.5%"],
            ["湮滅傷害加成", "30%", "攻擊100", "攻擊11.6%", "防禦10%", "普攻傷害加成8.6%", "暴擊8.1%", "暴擊傷害18.6%"],
            ["攻擊", "滿18%", "生命2280", "暴擊傷害17.4%", "共鳴技能傷害加成8.6%", "普攻傷害加成10.1%", "攻擊7.9%", "暴擊6.3%"],
            ["攻擊", "18%", "生命2280", "暴擊7.5%", "防禦8.1%", "攻擊7.9%", "暴擊傷害12.6%", "攻擊40"]
        ]

@pytest.mark.integration
def test_process_image():
    # Fake OCR 回傳物件
    fake_ocr_results = FakeOCRResults()
    # patch GoogleOCR.ocr 或 process_image 內呼叫 OCR 的地方
    with patch("generate_result.GoogleOCR.ocr", return_value=fake_ocr_results):
        dummy_img = Image.new("RGB", (100, 100), color="white")
        result = process_image(dummy_img)

        # 檢查回傳值
        assert "image" in result
        assert "result" in result
        assert "score" in result["result"]
        assert "rank" in result["result"]