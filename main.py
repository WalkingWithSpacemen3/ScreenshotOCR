import pytesseract
from win11toast import toast

text = "ass"
pytesseract.pytesseract.tesseract_cmd = r'F:\Program Files\Tesseract-OCR\tesseract'
available_option = pytesseract.get_languages(config='')
print(available_option)

def test_button(args):
    print(args['user_input']['selection'])
    print('clicked')


toast('Text Copied! (Click to Retry)', text, dialogue=text,
      on_click=test_button, selection=available_option[:5])
