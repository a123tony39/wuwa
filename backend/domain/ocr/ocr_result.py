from dataclasses import dataclass
@dataclass
class OCRResult:
    player_block: list[str]
    echo_block: list[list[str]] 