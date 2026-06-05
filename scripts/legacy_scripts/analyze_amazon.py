"""Analyze the Amazon dataset for the catalog rebuild."""
import csv
import re
import json

f = open(r'datasets\amazon_sales\amazon.csv', 'r', encoding='utf-8')
reader = csv.DictReader(f)
rows = list(reader)
f.close()

# Deduplicate by product_id
seen = set()
unique = []
for r in rows:
    if r['product_id'] not in seen:
        seen.add(r['product_id'])
        unique.append(r)

print(f"Total rows: {len(rows)}, Unique products: {len(unique)}")

# Parse prices (remove rupee symbol and commas)
def parse_price(price_str):
    cleaned = re.sub(r'[^\d.]', '', price_str.replace(',', ''))
    try:
        return float(cleaned) if cleaned else 0.0
    except:
        return 0.0

# Convert INR to USD (approximate)
INR_TO_USD = 0.012

good = []
for r in unique:
    price_inr = parse_price(r.get('discounted_price', ''))
    price_usd = round(price_inr * INR_TO_USD, 2)
    try:
        rating = float(r.get('rating', '0').strip())
    except:
        rating = 0.0
    try:
        rating_count = int(r.get('rating_count', '0').replace(',', '').strip())
    except:
        rating_count = 0
    
    img = r.get('img_link', '')
    name = r.get('product_name', '').strip()
    cat_full = r.get('category', '')
    top_cat = cat_full.split('|')[0] if '|' in cat_full else cat_full
    desc = r.get('about_product', '').strip()
    
    # Quality filters
    if price_usd < 2 or price_usd > 2000:
        continue
    if not img.startswith('http'):
        continue
    if not name or len(name) < 10:
        continue
    if rating < 3.0:
        continue
    if rating_count < 100:
        continue
    if not desc or len(desc) < 20:
        continue
    
    good.append({
        'product_id': r['product_id'],
        'name': name[:150],
        'top_category': top_cat,
        'full_category': cat_full,
        'price_usd': price_usd,
        'rating': rating,
        'rating_count': rating_count,
        'img_link': img,
        'description': desc[:500],
        'product_link': r.get('product_link', '')
    })

print(f"After quality filter: {len(good)} products")

# Category distribution
cats = {}
for p in good:
    cats[p['top_category']] = cats.get(p['top_category'], 0) + 1
print("\nCategory distribution:")
for k, v in sorted(cats.items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}")

# Price distribution
prices = [p['price_usd'] for p in good]
print(f"\nPrice range: ${min(prices):.2f} - ${max(prices):.2f}")
print(f"Median price: ${sorted(prices)[len(prices)//2]:.2f}")

# Show a few samples
print("\n--- Sample products ---")
for p in good[:3]:
    out = {k: (v[:80] if isinstance(v, str) and len(v) > 80 else v) for k, v in p.items()}
    print(json.dumps(out, ensure_ascii=True, indent=2))
