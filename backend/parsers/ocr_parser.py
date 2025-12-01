from dataclasses import dataclass, field
from typing import List

@dataclass
class Stat:
    name: str = ""
    value: float = 0.0

@dataclass
class EchoData:
    main_stat: Stat = field(default_factory=Stat)
    static_stat: Stat = field(default_factory=Stat)
    sub_stat: List[Stat] = field(default_factory=list)

PERCENTABLE = ["生命", "攻擊", "防禦"]
def parse_ocr_output(ocr_result) -> EchoData:
    print("-----------------------------")
    new_echo = EchoData()
    texts = []
    for _, text, prob in ocr_result:
        print(f"文字: {text}, 信心指數: {prob:.2f}")
        texts.append(text)

    pairs = [texts[i:i+2] for i in range(0, len(texts), 2)]
    
    for idx, (name, value) in enumerate(pairs):
        if idx == 0:
            new_echo.main_stat.name = name
            new_echo.main_stat.value = value # fix 
        elif idx == 1:
            new_echo.static_stat.name = name
            new_echo.static_stat.value = float(value.strip("%")) if '%' in value else float(value)
        else:
            new_echo.sub_stat.append(Stat(name=f"{name}%" if '%' in value and name in PERCENTABLE else name, value=float(value.strip("%")) if '%' in value else float(value)))
    return new_echo