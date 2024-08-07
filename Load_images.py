import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt


def url_to_image(imgUrl: str):
    res = requests.get(imgUrl)
    img = Image.open(BytesIO(res.content))
    return img
