import pytesseract
from PIL import Image

text = "ass"
pytesseract.pytesseract.tesseract_cmd = r'F:\Program Files\Tesseract-OCR\tesseract'
available_option = pytesseract.get_languages(config='')
print(available_option)


def tesseract_read_img(lang):
    text = pytesseract.image_to_string(Image.open('img.png'), lang=lang)
    print(text)
    return text


tesseract_read_img('jpn')
