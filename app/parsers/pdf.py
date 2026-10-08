import io
from pypdf import PdfReader
def parse(data):
 r=PdfReader(io.BytesIO(data));return '\n\n'.join(f'[PAGE {i}]\n{p.extract_text() or ""}' for i,p in enumerate(r.pages,1)),len(r.pages)
