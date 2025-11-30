from dataclasses import dataclass, field
from typing import List

@dataclass
class Stat:
    type: str = ""
    value: float = 0.0

@dataclass
class EchoData:
    main_stat: Stat = field(default_factory=Stat)
    static_stat: Stat = field(default_factory=Stat)
    sub_stat: List[Stat] = field(default_factory=list)

BAD_CHARS = ["文", "C", "+", "&", "F", " ", "*", "x", "戊"]

def parse_ocr_output(ocr_result) -> EchoData:
    print("-----------------------------")
    new_echo = EchoData()
    texts = []
    for bbox, text, prob in ocr_result:
        for b in BAD_CHARS:
            text = text.replace(b, "")
        print(f"文字: {text}, 信心指數: {prob:.2f}")
        texts.append(text)

    pairs = [texts[i:i+2] for i in range(0, len(texts), 2)]
    
    for idx, (name, value) in enumerate(pairs):
        if idx == 0:
            new_echo.main_stat.type = name
            new_echo.main_stat.value = value
        elif idx == 1:
            new_echo.static_stat.type = name
            new_echo.static_stat.value = value
        else:
            new_echo.sub_stat.append(Stat(type=name, value=value))
    return new_echo