import json,csv,io
def parse_text(data):return data.decode('utf-8-sig',errors='replace'),1
def parse_csv(data):return '\n'.join(' | '.join(r) for r in csv.reader(io.StringIO(data.decode('utf-8-sig',errors='replace')))),1
def parse_json(data):return json.dumps(json.loads(data.decode('utf-8-sig')),ensure_ascii=False,indent=2),1
