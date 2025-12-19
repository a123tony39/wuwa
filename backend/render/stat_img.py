from PIL import Image

def load_stat_img(stat_name, valid, STATS_NAME_MAP, is_sub_stat, img_path):
    folder = "sub_stat" if is_sub_stat else "main_stat"
    is_valid = "invalid" if stat_name not in valid else "valid"
    file = img_path / folder / is_valid / f"{STATS_NAME_MAP[stat_name]}.png"
    img = Image.open(file)
    return img