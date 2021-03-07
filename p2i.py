from typing import Optional
from pdf2image import convert_from_path
import os
import pytesseract
from PIL import Image


def pdf_to_image(
    path_to_file: str = "hat_1.pdf", path_to_store: Optional[str] = None
) -> bool:
    if not path_to_store:
        path_to_store = f"./{path_to_file.split('/')[-1].split('.pdf')[0]}"
        if not os.path.exists(path_to_store):
            os.makedirs(path_to_store)
    images = convert_from_path(path_to_file)
    for i in range(len(images)):
        images[i].save(f"{path_to_store}/page_{i}.jpg", "JPEG")
    return True


def image_to_text(filename: str):
    text = pytesseract.image_to_string(Image.open(filename))
    return text


pdf_to_image()
print(image_to_text("./hat_1/page_15.jpg"))
