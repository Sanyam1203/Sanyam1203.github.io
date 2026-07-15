import os
import re

files_meta = {
    'index.html': {
        'title': 'Saffire EV | Electric Three-Wheelers by Koyo Gears India Pvt. Ltd.',
        'desc': 'Saffire EV by Koyo Gears India Pvt. Ltd. builds electric cargo and passenger three-wheelers for Indian businesses, dealers, fleets and future-ready mobility.',
        'canonical': 'https://saffireev.com/',
        'og_title': 'Saffire EV | Electric Three-Wheelers by Koyo Gears India Pvt. Ltd.',
        'og_desc': 'Saffire EV by Koyo Gears India Pvt. Ltd. builds electric cargo and passenger three-wheelers for Indian businesses, dealers, fleets and future-ready mobility.'
    },
    'products/index.html': {
        'title': 'Electric Cargo and Passenger Three-Wheelers | Saffire EV',
        'desc': 'Explore Saffire EV electric cargo and passenger three-wheelers designed for range, durability, payload and business profitability.',
        'canonical': 'https://saffireev.com/products/',
        'og_title': 'Electric Cargo and Passenger Three-Wheelers | Saffire EV',
        'og_desc': 'Explore Saffire EV electric cargo and passenger three-wheelers designed for range, durability, payload and business profitability.'
    },
    'vision/index.html': {
        'title': 'Vision and Technology | Saffire EV',
        'desc': 'Discover the Saffire EV vision for intelligent, reliable and efficient electric mobility in India.',
        'canonical': 'https://saffireev.com/vision/',
        'og_title': 'Vision and Technology | Saffire EV',
        'og_desc': 'Discover the Saffire EV vision for intelligent, reliable and efficient electric mobility in India.'
    },
    'contact/index.html': {
        'title': 'Contact Saffire EV | Dealer, Pre-Order and Partnership Inquiries',
        'desc': 'Contact Saffire EV for electric vehicle dealership, pre-order, business partnership and product inquiries.',
        'canonical': 'https://saffireev.com/contact/',
        'og_title': 'Contact Saffire EV | Dealer, Pre-Order and Partnership Inquiries',
        'og_desc': 'Contact Saffire EV for electric vehicle dealership, pre-order, business partnership and product inquiries.'
    },
    'terms/index.html': {
        'title': 'Terms and Conditions | Saffire EV',
        'desc': 'Read the terms and conditions for using the Saffire EV website and services.',
        'canonical': 'https://saffireev.com/terms/',
        'og_title': 'Terms and Conditions | Saffire EV',
        'og_desc': 'Read the terms and conditions for using the Saffire EV website and services.'
    }
}

common_head_injections = """
<!-- SEO Optimization & Verification -->
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#131315">
<!-- Google Search Console verification meta tag goes here after token is provided -->
<!-- Bing Webmaster verification meta tag goes here after token is provided -->
<!-- Microsoft Clarity project ID goes here after project is created -->
"""

track_event_script = """
<script>
function trackEvent(eventName, params = {}) {
  if (typeof gtag === "function") {
    gtag("event", eventName, params);
  }
}
</script>
"""

for path, meta in files_meta.items():
    if not os.path.exists(path):
        continue
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update Title
    content = re.sub(r'<title>.*?</title>', f'<title>{meta["title"]}</title>', content, flags=re.DOTALL)
    
    # 2. Update Description
    if re.search(r'<meta[^>]*name="description"[^>]*>', content):
        content = re.sub(r'<meta[^>]*name="description"[^>]*>', f'<meta name="description" content="{meta["desc"]}">', content)
    else:
        content = content.replace('</head>', f'<meta name="description" content="{meta["desc"]}">\n</head>')

    # 3. Update Canonical
    if re.search(r'<link[^>]*rel="canonical"[^>]*>', content):
        content = re.sub(r'<link[^>]*rel="canonical"[^>]*>', f'<link rel="canonical" href="{meta["canonical"]}">', content)
    else:
        content = content.replace('</head>', f'<link rel="canonical" href="{meta["canonical"]}">\n</head>')

    # 4. Open Graph Tags
    # Clean up old OG tags
    content = re.sub(r'<meta[^>]*property="og:(title|description|image|url|type)"[^>]*>', '', content)
    
    og_image = "https://saffireev.com/images/herobanner.png" if "index.html" in path else "https://saffireev.com/images/herobanner.png" # Standardizing
    og_tags = f"""
<meta property="og:title" content="{meta['og_title']}">
<meta property="og:description" content="{meta['og_desc']}">
<meta property="og:image" content="{og_image}">
<meta property="og:url" content="{meta['canonical']}">
<meta name="twitter:title" content="{meta['og_title']}">
<meta name="twitter:description" content="{meta['og_desc']}">
<meta name="twitter:image" content="{og_image}">
"""
    content = content.replace('</head>', f'{og_tags}\n{common_head_injections}\n{track_event_script}\n</head>')

    # 5. Add specific schemas
    if path == 'index.html':
        website_schema = """
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Saffire EV",
  "url": "https://saffireev.com/",
  "publisher": {
    "@type": "Organization",
    "name": "Koyo Gears India Pvt. Ltd."
  }
}
</script>
"""
        content = content.replace('</head>', f'{website_schema}\n</head>')
    
    if path == 'products/index.html':
        product_schema = """
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "itemListElement": [
    {
      "@type": "Product",
      "name": "Electric Cargo Three-Wheeler",
      "brand": {
        "@type": "Brand",
        "name": "Saffire EV"
      }
    },
    {
      "@type": "Product",
      "name": "Electric Passenger Three-Wheeler",
      "brand": {
        "@type": "Brand",
        "name": "Saffire EV"
      }
    }
  ]
}
</script>
"""
        content = content.replace('</head>', f'{product_schema}\n</head>')

    # 6. Add loading="lazy" decoding="async" to images below fold
    # Using simple regex, we avoid the hero image by matching herobanner.png
    def img_repl(match):
        img_tag = match.group(0)
        if 'herobanner.png' in img_tag or 'logo' in img_tag:
            return img_tag
        if 'loading="lazy"' not in img_tag:
            img_tag = img_tag.replace('<img ', '<img loading="lazy" decoding="async" ')
        return img_tag

    content = re.sub(r'<img[^>]*>', img_repl, content)

    # 7. Button Tracking Additions
    # Helper to add onClick event to anchors and buttons
    def add_tracking(html, text_match, event_name, params):
        # find matching <a> or <button> that contains text_match and add onclick
        # Very simple regex for href="..." or class="..." containing text
        pass

    # For index.html
    if path == 'index.html':
        content = content.replace('href="contact/" class="kinetic-gradient', 'href="contact/" onclick="trackEvent(\'preorder_click\', {page_name: \'home\'})" class="kinetic-gradient')
        content = content.replace('href="contact/?type=dealer"', 'href="contact/?type=dealer" onclick="trackEvent(\'dealer_cta_click\', {page_name: \'home\'})"')
        content = content.replace('setFuel(\'diesel\')', 'trackEvent(\'calculator_fuel_toggle\', {fuel_type: \'diesel\'}); setFuel(\'diesel\')')
        content = content.replace('setFuel(\'petrol\')', 'trackEvent(\'calculator_fuel_toggle\', {fuel_type: \'petrol\'}); setFuel(\'petrol\')')

    if path == 'products/index.html':
        content = content.replace('href="/contact"', 'href="/contact" onclick="trackEvent(\'preorder_click\', {page_name: \'products\'})" ')

    if path == 'vision/index.html':
        content = content.replace('href="/contact"', 'href="/contact" onclick="trackEvent(\'contact_click\', {page_name: \'vision\'})" ')
    
    # 8. Contact Form specific enhancements
    if path == 'contact/index.html':
        # Add action to form
        content = content.replace('<form id="saffire-contact-form" class="space-y-6 md:space-y-8">',
                                  '<form id="saffire-contact-form" action="https://formspree.io/f/xnjolggl" method="POST" class="space-y-6 md:space-y-8">\n<input type="hidden" name="_subject" value="New Saffire EV Website Inquiry">\n<input type="hidden" name="source_page" value="contact">')
        # Add tracking to fetch
        content = content.replace("document.getElementById('thank-you-msg').classList.remove('hidden');", 
                                  "document.getElementById('thank-you-msg').classList.remove('hidden');\n                    trackEvent('contact_form_submit', {form_type: 'business_inquiry'});")
        content = content.replace("btn.textContent = 'Error — Retry';",
                                  "btn.textContent = 'Error — Retry';\n                    trackEvent('form_error', {form_type: 'business_inquiry'});")

    # Clean up empty lines created by regex
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print("SEO update applied successfully.")
