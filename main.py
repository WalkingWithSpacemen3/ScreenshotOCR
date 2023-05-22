import asyncio
import os
import pickle
import platform
import time

import easyocr
import pyperclip
import pytesseract
from PIL import Image
from win11toast import toast

folder_path = 'F:\Data\PicPickPics'
pytesseract.pytesseract.tesseract_cmd = r'F:\Program Files\Tesseract-OCR\tesseract'
available_option = pytesseract.get_languages(config='')
current_path = str()
if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


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


def tesseract_read_img(lang):
    text = pytesseract.image_to_string(Image.open(current_path), lang=lang).replace('\n', ' ')
    print(text)
    return text


def retry(args):
    print(args)
    copy_to_clipboard(tesseract_read_img(args['user_input']['selection']))


def copy_to_clipboard(text):
    pyperclip.copy(text)
    toast('Text Copied! (Click to Retry)', text,
          on_click=retry, selection=available_option[:5])


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
        current_path = f
        result = tesseract_read_img('eng')
        copy_to_clipboard(result)
    last_files = files
    time.sleep(1)
    with open('files.pkl', 'wb') as f:
        pickle.dump(last_files, f)
