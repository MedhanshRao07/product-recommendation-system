"""Quick inspection script for the Amazon 2023 archive."""
import zipfile, csv, io

z = zipfile.ZipFile('archive (4).zip')

# Check structure of a few key files
target_files = [
    'All Electronics.csv',
    'All Home and Kitchen.csv',
    'All Appliances.csv',
    'Headphones.csv',
    'Cameras.csv',
]

for fname in target_files:
    try:
        f = z.open(fname)
        reader = csv.DictReader(io.TextIOWrapper(f, 'utf-8'))
        rows = []
        for i, row in enumerate(reader):
            if i >= 3:
                break
            rows.append(row)
        
        print(f"\n=== {fname} ({len(rows)} sample rows) ===")
        if rows:
            print(f"Columns: {list(rows[0].keys())}")
            for r in rows[:1]:
                for k, v in r.items():
                    print(f"  {k}: {repr(v[:100]) if isinstance(v, str) and len(v) > 100 else repr(v)}")
        f.close()
    except Exception as e:
        print(f"Error reading {fname}: {e}")

# Count rows in key files
print("\n\n=== ROW COUNTS ===")
count_files = [
    'All Electronics.csv',
    'All Home and Kitchen.csv', 
    'All Appliances.csv',
    'Headphones.csv',
    'Cameras.csv',
    'Home Entertainment Systems.csv',
    'Speakers.csv',
    'Kitchen and Home Appliances.csv',
    'Kitchen and Dining.csv',
    'Televisions.csv',
    'Watches.csv',
    'Shoes.csv',
    'Sports Shoes.csv',
    'Fitness Accessories.csv',
    'Backpacks.csv',
    'Sunglasses.csv',
    'Camera Accessories.csv',
    'Security Cameras.csv',
    'Heating and Cooling Appliances.csv',
]

for fname in count_files:
    try:
        f = z.open(fname)
        reader = csv.reader(io.TextIOWrapper(f, 'utf-8'))
        next(reader)  # skip header
        count = sum(1 for _ in reader)
        print(f"  {fname}: {count} rows")
        f.close()
    except Exception as e:
        print(f"  {fname}: ERROR - {e}")

z.close()
