import os
import re

frontend_dir = r'c:\Users\medha\OneDrive\Desktop\product_rec\frontend\src'

for root, _, files in os.walk(frontend_dir):
    for f in files:
        if f.endswith(('.jsx', '.js')):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            orig_content = content
            
            # Fix single-quoted interpolations:
            # '${process.env.REACT_APP_API_URL || 'http://localhost:5000'}/api/products' ->
            # `${process.env.REACT_APP_API_URL || 'http://localhost:5000'}/api/products`
            content = re.sub(
                r"'(\$\{process\.env\.REACT_APP_API_URL \|\| 'http://localhost:5000'\}[^']+)'",
                r"`\1`",
                content
            )
            
            # Fix the Chatbot mess
            chatbot_mess = r"`\$\{process\.env\.REACT_APP_API_URL \|\| 'http://localhost:5000'\}` \|\| 'http://localhost:5000'\}/api/chat'"
            chatbot_fix = r"`${process.env.REACT_APP_API_URL || 'http://localhost:5000'}/api/chat`"
            content = content.replace(chatbot_mess, chatbot_fix)
            
            if content != orig_content:
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f'Fixed {f}')
