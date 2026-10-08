def chunk_text(text,size=900,overlap=150):
 if not text.strip():return []
 if overlap>=size:raise ValueError('overlap must be smaller than size')
 out=[];start=0
 while start<len(text):
  end=min(len(text),start+size); piece=text[start:end].strip()
  if piece:out.append(piece)
  if end==len(text):break
  start=end-overlap
 return out
