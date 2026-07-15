import os
import glob

html_files = [
    'index.html',
    'products/index.html',
    'vision/index.html',
    'contact/index.html',
    'terms/index.html',
    '404.html'
]

bing_meta = '<meta name="msvalidate.01" content="D334E6EBCA70575B360E942A1A5E4D8E" />'
placeholder = '<!-- Bing Webmaster verification meta tag goes here after token is provided -->'

for file in html_files:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if placeholder in content:
            content = content.replace(placeholder, bing_meta)
        elif bing_meta not in content:
            # If placeholder isn't there, just insert it before </head>
            content = content.replace('</head>', f'{bing_meta}\n</head>')
            
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)

