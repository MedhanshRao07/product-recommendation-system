import urllib.request
import json

url = 'http://localhost:5000/api/products/grouped'
req = urllib.request.Request(url)
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        print('Sample category images:')
        for cat, items in list(data.items())[:3]:
            print(f'{cat}:')
            for item in items:
                img = item.get('image_url', '').split('/')[-1]
                print(f"  - {item['name']} -> {img}")
except Exception as e:
    print(e)
