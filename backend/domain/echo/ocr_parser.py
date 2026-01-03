import re
from typing import List
from dataclasses import dataclass, field

@dataclass
class Stat:
    name: str = ""
    value: float = 0.0

@dataclass
class EchoData:
    main_stat: Stat = field(default_factory=Stat)
    static_stat: Stat = field(default_factory=Stat)
    sub_stat: List[Stat] = field(default_factory=list)


def normalize(text):
    VALID_STATS = ["暴擊傷害", "暴擊", "攻擊", "生命", "防禦", "共鳴效率", "普攻傷害加成", "共鳴解放傷害加成", "重擊傷害加成", "共鳴技能傷害加成"]
    for stat in VALID_STATS:
        if stat in text:
            return stat
    return text # value

PERCENTABLE = ["生命", "攻擊", "防禦"]
def parse_ocr_output(ocr_result) -> EchoData:
    print("-----------------------------")
    new_echo = EchoData()
    texts = []

    # get main stat
    for text in ocr_result[:2]:
        text = normalize(text)
        print(f"文字: {text}")
        texts.append(text)
        
    # get sub stat
    for text in ocr_result[2:]:
        stat = normalize(text)
        name = stat
        value = text[len(stat):]
        print(f"文字: {stat}")
        print(f"文字: {value}")
        texts.append(stat)
        texts.append(value)

    pairs = [texts[i:i+2] for i in range(0, len(texts), 2)]
    for idx, (name, value) in enumerate(pairs):
        print(name, value)
        name, value = parse_stat_pair(name, value, PERCENTABLE)
        if idx == 0:
            new_echo.main_stat.name = name 
            new_echo.main_stat.value = value
        elif idx == 1:
            new_echo.static_stat.name = name
            new_echo.static_stat.value = value
        else:
            new_echo.sub_stat.append(Stat(name=name, value=value))
    return new_echo


def parse_stat_pair(name, value, percentable):
    if '%' in value and name in percentable:
        name = f"{name}%" 
    match = re.findall(r'\d+\.?\d*%?', value)
    if not match:
        raise ValueError(f"Invalid value: {value}")
    
    raw = match[-1]
    val = float(raw.strip("%"))

    return name, val