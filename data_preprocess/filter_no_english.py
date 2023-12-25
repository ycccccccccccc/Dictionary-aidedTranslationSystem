import json

raw_data_path = '../raw/F01-10000-0102.json'
filtered_data_path = '../filtered/F01-10000-0102.json'

with open(raw_data_path, 'r') as json_file:
    raw_data = json.load(json_file)['gpss-API']['patent']['patentcontent']

results = []

for data in raw_data:

    if 'abstract' not in data:
        continue

    if not isinstance( data['abstract']['p'], list):
        continue
    
    if len(data['abstract']['p'])!=2:
        continue

    if not 'english-title' in data['patent-title'] or 'title' not in data['patent-title']:
        continue
    if len(data['abstract']['p'][1]) < 2:
        continue
    


    results.append({
        'doc-number': data['publication-reference']['doc-number'],
        'title':{
            'en': data['patent-title']['english-title'],
            'zh': data['patent-title']['title'],
        },
        'abstract': {
            'en': data['abstract']['p'][1],
            'zh': data['abstract']['p'][0],
        }
    })
with open(filtered_data_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

    
print("==== STATISTICS ====")
print(f'RAW: {len(raw_data)}')
print(f'FILTERED: {len(results)}')