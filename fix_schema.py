import re
import os

files_to_check = [
    'products/index.html',
    'electric-cargo-loader/index.html',
    'electric-passenger-auto/index.html'
]

safe_itemlist = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "Saffire EV Vehicle Categories",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Electric Cargo Three-Wheeler",
      "url": "https://saffireev.com/electric-cargo-loader/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Electric Passenger Three-Wheeler",
      "url": "https://saffireev.com/electric-passenger-auto/"
    }
  ]
}
</script>"""

for path in files_to_check:
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find all JSON-LD scripts
        scripts = re.finditer(r'<script\s+type="application/ld\+json">.*?</script>', content, flags=re.DOTALL)
        
        for match in scripts:
            script_content = match.group(0)
            
            # If it's products/index.html and contains Product schema
            if path == 'products/index.html' and '"@type": "Product"' in script_content:
                content = content.replace(script_content, safe_itemlist)
            
            # If it's one of the other pages and contains Product schema, remove it entirely
            elif path != 'products/index.html' and '"@type": "Product"' in script_content:
                content = content.replace(script_content, '')
        
        # Clean up possible extra newlines left by removal
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

print("Schema fixed successfully.")
