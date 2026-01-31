from abc import ABC, abstractmethod
from PIL import Image
from typing import List, Tuple
from dataclasses import dataclass

OCR_CROP_AREAS = [ 
    (0, 0, 300, 150),
    (60, 710, 380, 1050),
    (440, 710, 380*2, 1050),
    (815, 710, 380*3, 1050),
    (1190, 710, 380*4, 1050),
    (1560, 710, 380*5, 1050)
]

@dataclass
class OCRResult:
    player_block: list[str]
    echo_block: list[list[str]] 

class OCRService(ABC):
    @abstractmethod
    def recognize(
        self,
        image: Image.Image,
        crop_areas: List[Tuple],
    ) -> OCRResult:
        pass