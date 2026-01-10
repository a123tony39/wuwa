import pytest
from unittest.mock import patch
from generate_result import process_image
from infrastructure.yaml_io import load_yaml
from PIL import Image

class FakeOCR:
    def recognize(self, source, crop_area):
        return FakeOCRResults()
    
class FakeOCRResults:
    def __init__(self):
        test_ocr_results = load_yaml("./tests/test_fixtures/ocr_result.yaml")
        self.player_block = test_ocr_results['player_block']
        self.echo_block = test_ocr_results['echo_block']
        
@pytest.mark.integration
def test_process_image():
    # Fake OCR 回傳物件
    fake_ocr = FakeOCR()
    # patch GoogleOCR.ocr
    dummy_img = Image.new("RGB", (100, 100), color="white")
    result = process_image(dummy_img, fake_ocr)

    # 檢查回傳值
    assert "image" in result
    assert "result" in result
    assert "score" in result["result"]
    assert "rank" in result["result"]