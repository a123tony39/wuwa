import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

def load_yaml(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def background_exists(character_name: str) -> bool:
    path = BASE_DIR / "img" / "background" / f"{character_name}.png"
    return path.is_file()

def avatar_exists(character_name: str) -> bool:
    path = BASE_DIR / "img" / "character" / f"{character_name}.png"
    return path.is_file()

    
# def test_character_assets_exist():
#     print(BASE_DIR)
#     character_path = BASE_DIR / "backend" / "scoring" / "character_template.yaml"
#     character_template = load_yaml(character_path)
    
#     missing = []

#     for _, info in character_template.items():
#         character_en = info["en"]
#         if not background_exists(character_en):
#             missing.append(f"{character_en}: background")
#         if not avatar_exists(character_en):
#             missing.append(f"{character_en}: avatar")

#     assert not missing, "Missing assets: \n" + "\n".join(missing)