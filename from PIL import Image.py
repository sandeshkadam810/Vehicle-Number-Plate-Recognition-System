from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
im = Image.open('C:/Users/SANDESH/Documents/psap c/VS Code programs/5.jpeg')
text = pytesseract.image_to_string(im, lang = 'eng')
print(text)
