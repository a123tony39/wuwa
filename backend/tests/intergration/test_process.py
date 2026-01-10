import pytest
from PIL import Image
from generate_result import process_image
from infrastructure.yaml_io import load_yaml

class FakeOCR:
    def recognize(self, _, __):
        return FakeOCRResults()
    
class FakeOCRResults:
    def __init__(self):
        test_ocr_results = load_yaml("./tests/test_fixtures/ocr_result.yaml")
        self.player_block = test_ocr_results['player_block']
        self.echo_block = test_ocr_results['echo_block']

@pytest.mark.integration
def test_process_image():
    fake_ocr = FakeOCR()
    dummy_img = Image.new("RGB", (100, 100), color="white")
    result = process_image(dummy_img, fake_ocr)

    assert "image" in result
    assert "result" in result
    assert "score" in result["result"]
    assert "rank" in result["result"]