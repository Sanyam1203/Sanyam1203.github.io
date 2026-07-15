import os
import re

files = [
    'index.html',
    'products/index.html',
    'vision/index.html',
    'contact/index.html',
    'terms/index.html'
]

def check_file(path):
    if not os.path.exists(path):
        return f"{path} - MISSING"
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    ga = re.search(r'G-[A-Z0-9]+', content)
    form = re.search(r'<form[^>]*action="([^"]*)"', content)
    title = re.search(r'<title>(.*?)</title>', content)
    desc = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]*)"', content)
    canonical = re.search(r'<link[^>]*rel="canonical"[^>]*href="([^"]*)"', content)
    og_title = re.search(r'<meta[^>]*property="og:title"[^>]*content="([^"]*)"', content)
    twitter_card = re.search(r'<meta[^>]*name="twitter:card"', content)
    schema = re.search(r'application/ld\+json', content)
    
    return {
        'path': path,
        'ga': ga.group(0) if ga else 'Missing',
        'form_action': form.group(1) if form else 'No Form',
        'title': title.group(1) if title else 'Missing',
        'desc': desc.group(1) if desc else 'Missing',
        'canonical': canonical.group(1) if canonical else 'Missing',
        'og_title': og_title.group(1) if og_title else 'Missing',
        'twitter_card': 'Present' if twitter_card else 'Missing',
        'schema': 'Present' if schema else 'Missing'
    }

for file in files:
    res = check_file(file)
    if isinstance(res, str):
        print(res)
    else:
        print(f"--- {res['path']} ---")
        print(f"GA4: {res['ga']}")
        print(f"Form Action: {res['form_action']}")
        print(f"Title: {res['title']}")
        print(f"Desc: {res['desc']}")
        print(f"Canonical: {res['canonical']}")
        print(f"OG Title: {res['og_title']}")
        print(f"Twitter Card: {res['twitter_card']}")
        print(f"Schema: {res['schema']}")

print("--- 404.html ---")
print("Exists:", os.path.exists('404.html'))

