"""Test all API endpoints."""
import urllib.request
import json

BASE = 'http://localhost:5000'

def test(name, url):
    try:
        r = urllib.request.urlopen(url)
        data = json.loads(r.read())
        if isinstance(data, list):
            print(f'[OK] {name}: {len(data)} items')
        elif isinstance(data, dict):
            if 'products' in data:
                print(f'[OK] {name}: {len(data["products"])} products (total: {data.get("total", "N/A")})')
            elif 'recommendations' in data:
                print(f'[OK] {name}: {len(data["recommendations"])} recommendations')
            else:
                print(f'[OK] {name}: {data}')
        else:
            print(f'[OK] {name}: {data}')
    except Exception as e:
        print(f'[FAIL] {name}: {e}')

def test_post(name, url, body):
    try:
        req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'})
        r = urllib.request.urlopen(req)
        data = json.loads(r.read())
        if 'recommendations' in data:
            print(f'[OK] {name}: {len(data["recommendations"])} recommendations')
        else:
            print(f'[OK] {name}: {data}')
    except Exception as e:
        print(f'[FAIL] {name}: {e}')

print('=== API ENDPOINT TESTS ===\n')

# Products (no pagination - existing behavior)
test('GET /api/products (all)', f'{BASE}/api/products')

# Products (paginated)
test('GET /api/products?page=1&per_page=10', f'{BASE}/api/products?page=1&per_page=10')

# Trending
test('GET /api/products/trending', f'{BASE}/api/products/trending')

# Categories
test('GET /api/products/categories', f'{BASE}/api/products/categories')

# Search
test('GET /api/products/search?q=Nike', f'{BASE}/api/products/search?q=Nike')
test('GET /api/products/search?q=laptop', f'{BASE}/api/products/search?q=laptop')

# Category filter
test('GET /api/products/category/Electronics', f'{BASE}/api/products/category/Electronics')
test('GET /api/products/category/Shoes', f'{BASE}/api/products/category/Shoes')

# Recommendations (POST)
test_post('POST /api/products/recommend (Electronics, $500, 4.0)',
    f'{BASE}/api/products/recommend',
    {'category': 'Electronics', 'max_price': 500, 'rating': 4.0})

# Auto-recommend
test('GET /api/products/auto-recommend/1', f'{BASE}/api/products/auto-recommend/1')

# ChatBot
test_post('POST /api/chat', f'{BASE}/api/chat', {'message': 'Hello', 'history': []})

# Health
test('GET /health', f'{BASE}/health')

print('\nDone!')
