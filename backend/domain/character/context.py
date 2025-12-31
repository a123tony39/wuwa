from dataclasses import dataclass

@dataclass
class CharacterContext:
    zh_name: str
    en_name: str
    template: dict
    valid_stats: set
    role: str