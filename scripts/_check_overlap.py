"""Check ASIN overlap between amazon.csv and Amazon 2023 zip"""
import zipfile
import csv
import io
import re

# 1. Get ASINs from amazon.csv
sales_asins = set()
try:
    with open('datasets/amazon_sales/amazon.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sales_asins.add(row['product_id'])
    print(f"Found {len(sales_asins)} unique ASINs in amazon.csv")
except Exception as e:
    print(f"Error reading amazon.csv: {e}")

# 2. Get ASINs from a few large 2023 files
zip_asins = set()
target_files = [
    'All Electronics.csv',
    'All Home and Kitchen.csv',
    'All Appliances.csv',
    'Headphones.csv',
    'Cameras.csv',
    'Televisions.csv',
    'Watches.csv',
    'Shoes.csv'
]

asin_pattern = re.compile(r'/([A-Z0-9]{10})(?:/|\?|$)')

try:
    with zipfile.ZipFile('archive (4).zip') as z:
        for fname in target_files:
            try:
                with z.open(fname) as f:
                    reader = csv.DictReader(io.TextIOWrapper(f, 'utf-8', errors='ignore'))
                    for row in reader:
                        link = row.get('link', '')
                        match = asin_pattern.search(link)
                        if match:
                            zip_asins.add(match.group(1))
            except Exception as e:
                print(f"Error reading {fname} from zip: {e}")
    print(f"Found {len(zip_asins)} unique ASINs in sampled 2023 files")
except Exception as e:
    print(f"Error reading zip: {e}")

# 3. Intersection
overlap = sales_asins.intersection(zip_asins)
print(f"Overlap: {len(overlap)} ASINs")
