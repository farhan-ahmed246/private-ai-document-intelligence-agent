import io,pytesseract
from PIL import Image
def image_to_text(data):return pytesseract.image_to_string(Image.open(io.BytesIO(data)))
