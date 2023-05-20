import os
import pickle
import time

import easyocr
import pyperclip
import pytesseract
from PIL import Image
from win11toast import toast

folder_path = 'F:\Data\PicPickPics'
pytesseract.pytesseract.tesseract_cmd = r'F:\Program Files\Tesseract-OCR\tesseract'
available_option = pytesseract.get_languages(config='')


def load_last_files():
    try:
        with open('files.pkl', 'rb') as f:
            last_files = pickle.load(f)
    except FileNotFoundError:
        last_files = set()
    return last_files


def easyocr_read_img(path):
    reader = easyocr.Reader(['en', 'ja'])
    raw_result = reader.readtext(path, detail=0)
    print(f'raw result: {raw_result}')
    text = ' '.join(reader.readtext(path, detail=0))
    return text


def tesseract_read_img(path):
    text = pytesseract.image_to_string(Image.open(path))
    print(text)
    return text


def test_button():
    print('clicked')


def copy_to_clipboard(text):
    pyperclip.copy(text)
    toast('Text Copied!', text, dialogue=text, button={'activationType': 'protocol','arguments': 'https://google.com', 'content': 'Open Google'})


def scan_files():
    files = {f.path for f in os.scandir(folder_path)}
    last_files = load_last_files()
    new_files = files.difference(last_files)
    return new_files, files


last_files = load_last_files()
while True:
    new_files, files = scan_files()
    # print(f'last files: {files}')
    for f in new_files:
        result = tesseract_read_img(f)
        copy_to_clipboard(result)
    last_files = files
    time.sleep(1)
    with open('files.pkl', 'wb') as f:
        pickle.dump(last_files, f)
