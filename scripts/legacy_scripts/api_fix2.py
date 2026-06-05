import os

frontend_dir = r'c:\Users\medha\OneDrive\Desktop\product_rec\frontend\src'

bad_pattern_1 = r"\'${process.env.REACT_APP_API_URL || (process.env.REACT_APP_API_URL || 'http://localhost:5000')}"
good_pattern_1 = r"`${process.env.REACT_APP_API_URL || 'http://localhost:5000'}"

bad_pattern_2 = r"${process.env.REACT_APP_API_URL || (process.env.REACT_APP_API_URL || 'http://localhost:5000')}"
good_pattern_2 = r"${process.env.REACT_APP_API_URL || 'http://localhost:5000'}"

bad_pattern_3 = r"}'/api"
good_pattern_3 = r"}/api"

for root, _, files in os.walk(frontend_dir):
    for f in files:
        if f.endswith(('.jsx', '.js')):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            orig_content = content
            content = content.replace(bad_pattern_1, good_pattern_1)
            content = content.replace(bad_pattern_2, good_pattern_2)
            content = content.replace("}'/api", "`/api")
            content = content.replace("}'/product", "`/product")
            
            if content != orig_content:
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f'Fixed {f}')
