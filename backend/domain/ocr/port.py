from abc import ABC, abstractmethod
from PIL import Image
from typing import List, Tuple
from .ocr_result import OCRResult

class OCRService(ABC):
    @abstractmethod
    def recognize(
        self,
        image: Image.Image,
        crop_areas: List[Tuple],
    ) -> OCRResult:
        pass