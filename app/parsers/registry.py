from pathlib import Path
from app.parsers.pdf import parse as pdf
from app.parsers.docx import parse as docx
from app.parsers.xlsx import parse as xlsx
from app.parsers.text import parse_text,parse_csv,parse_json
from app.ocr import image_to_text
from app.exceptions import ServiceError
def parse_document(name,data):
 e=Path(name).suffix.lower()
 if e=='.pdf':return pdf(data)
 if e=='.docx':return docx(data)
 if e=='.xlsx':return xlsx(data)
 if e=='.csv':return parse_csv(data)
 if e=='.json':return parse_json(data)
 if e in {'.txt','.md','.log'}:return parse_text(data)
 if e in {'.png','.jpg','.jpeg','.tiff','.tif','.bmp','.webp'}:return image_to_text(data),1
 raise ServiceError('Unsupported file type: '+e)
