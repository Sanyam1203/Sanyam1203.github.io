import os
import re

html_files = [
    'index.html',
    'products/index.html',
    'vision/index.html',
    'contact/index.html',
    'terms/index.html',
    '404.html'
]

new_footer = """<footer class="bg-[#0E0E10] border-t border-[#3B494C]/15 mt-auto">
    <div class="max-w-screen-2xl mx-auto px-8 md:px-12 py-10 md:py-16">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-10 mb-10">
            <!-- Brand -->
            <div class="flex flex-col items-center md:items-start text-center md:text-left">
                <span class="text-2xl font-bold tracking-tighter text-[#97FDFF] uppercase font-headline mb-1">SAFFIRE</span>
                <span class="text-[8px] md:text-[9px] tracking-[0.3em] text-slate-500 font-label">BY KOYO GEARS INDIA PRIVATE LIMITED</span>
            </div>
            <!-- Quick Links -->
            <div class="flex flex-col items-center md:items-start text-center md:text-left">
                <span class="font-label text-xs tracking-widest uppercase text-on-surface mb-4">Company</span>
                <a href="/products/" class="text-sm font-light text-slate-400 hover:text-white mb-2 transition-colors">Products</a>
                <a href="/vision/" class="text-sm font-light text-slate-400 hover:text-white mb-2 transition-colors">Vision</a>
                <a href="/contact/" class="text-sm font-light text-slate-400 hover:text-white mb-2 transition-colors">Contact</a>
            </div>
            <!-- EV Guides -->
            <div class="flex flex-col items-center md:items-start text-center md:text-left">
                <span class="font-label text-xs tracking-widest uppercase text-on-surface mb-4">EV Guides</span>
                <a href="/electric-cargo-loader/" class="text-sm font-light text-slate-400 hover:text-white mb-2 transition-colors">Electric Cargo Loader</a>
                <a href="/electric-passenger-auto/" class="text-sm font-light text-slate-400 hover:text-white mb-2 transition-colors">Electric Passenger Auto</a>
                <a href="/l5-electric-vehicle/" class="text-sm font-light text-slate-400 hover:text-white mb-2 transition-colors">L5 Electric Vehicle</a>
                <a href="/ev-dealership-india/" class="text-sm font-light text-slate-400 hover:text-white mb-2 transition-colors">EV Dealership in India</a>
                <a href="/electric-three-wheeler-running-cost/" class="text-sm font-light text-slate-400 hover:text-white transition-colors">Running Cost</a>
            </div>
        </div>
        
        <div class="border-t border-[#3B494C]/15 pt-6 flex flex-col md:flex-row justify-between items-center gap-6">
            <div class="text-slate-500 font-label text-[9px] md:text-[10px] tracking-[0.05em] uppercase text-center md:text-left">
                © 2026 KOYO GEARS INDIA PRIVATE LIMITED. ALL RIGHTS RESERVED.
            </div>
            <div class="flex flex-wrap justify-center gap-6">
                <a class="font-label text-[10px] md:text-xs uppercase tracking-[0.05em] text-slate-500 hover:text-white transition-opacity" href="/terms/">Privacy</a>
                <a class="font-label text-[10px] md:text-xs uppercase tracking-[0.05em] text-slate-500 hover:text-white transition-opacity" href="/terms/">Terms</a>
            </div>
        </div>
    </div>
</footer>"""

for path in html_files:
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Regex to find existing footer and replace it
        content = re.sub(r'<footer[^>]*>.*?</footer>', new_footer, content, flags=re.DOTALL)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
            
print("Footers updated.")
