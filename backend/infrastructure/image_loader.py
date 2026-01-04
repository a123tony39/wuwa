from PIL import Image

def load_img(file):
    return Image.open(file).convert("RGBA")