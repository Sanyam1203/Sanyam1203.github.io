import os
import re

files = [
    "index.html",
    "products/index.html",
    "vision/index.html",
    "contact/index.html",
    "terms/index.html"
]

def process_file(filepath):
    if not os.path.exists(filepath):
        print(f"Skipping {filepath}, does not exist.")
        return

    with open(filepath, 'r') as f:
        content = f.read()

    # Determine path prefix
    prefix = "" if filepath == "index.html" else "../"

    # 1. Add CSS
    css_link = f'<link href="{prefix}assets/css/motion.css" rel="stylesheet"/>'
    if css_link not in content:
        content = content.replace("</head>", f"    {css_link}\n</head>")

    # 2. Add JS
    js_link = f'<script src="{prefix}assets/js/motion.js"></script>'
    if js_link not in content:
        content = content.replace("</body>", f"    {js_link}\n</body>")

    # 3. Clean CSS
    # Remove transition-transform and scale from images
    content = re.sub(r'(class="[^"]*?)(\btransition-transform\b|\bgroup-hover:scale-105\b|\bhover:scale\b)([^"]*?")', 
                     lambda m: m.group(1) + m.group(3), content)
    # run twice to catch multiple matches in same string
    content = re.sub(r'(class="[^"]*?)(\btransition-transform\b|\bgroup-hover:scale-105\b|\bhover:scale\b)([^"]*?")', 
                     lambda m: m.group(1) + m.group(3), content)
    
    # Also clean up multiple spaces left behind
    content = re.sub(r'class="([^"]*)\s{2,}([^"]*)"', r'class="\1 \2"', content)

    # Remove the pageSwipeIn animation block
    content = re.sub(r'@keyframes pageSwipeIn\s*\{[^}]*\}\s*\.pageSwipeIn\s*\{[^}]*\}', '', content)
    content = re.sub(r'pageSwipeIn', '', content)

    # Clean up index.html specific transform in style
    if "index.html" in filepath:
        content = content.replace("transition: opacity 0.7s ease, transform 1s cubic-bezier(0.16,1,0.3,1);", "transition: opacity 0.7s ease;")

    # 4. Reveal replacements
    # Specific targeted replacements for cards to reveal-fade
    content = content.replace("min-h-[450px] fade-up", "min-h-[450px] premium-card reveal-fade")
    content = content.replace("overflow-hidden group fade-up", "overflow-hidden group premium-card reveal-fade")
    content = content.replace("fade-up", "reveal-text")

    # 5. Remove IntersectionObserver inline script
    content = re.sub(r'<script>\s*document\.addEventListener\("DOMContentLoaded", \(\) => \{\s*const observer = new IntersectionObserver[\s\S]*?\}\);\s*</script>', '', content)
    
    # specific contact page observer
    content = re.sub(r'const observer = new IntersectionObserver[\s\S]*?\.observe\(el\)\);\s*', '', content)

    # 6. Buttons
    # Change active:scale to transition filter instead if it's on a button, or just leave it since the global rule doesn't touch buttons.
    # But user said: "Do not scale button". So let's remove active:scale-[0.97]
    content = content.replace("active:scale-[0.97]", "")

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Processed {filepath}")

for f in files:
    process_file(f)
