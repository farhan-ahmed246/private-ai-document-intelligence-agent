import hashlib,uuid
def document_id(data):return hashlib.sha256(data).hexdigest()
def point_id(doc,index):return str(uuid.uuid5(uuid.NAMESPACE_URL,f'{doc}:{index}'))
