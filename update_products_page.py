import re
import os

filepath = 'products/index.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# We need to replace the section starting at <!-- Product Grid -->
# And ends before <!-- Future Vehicles Roadmap -->

new_section = """<!-- Product Grid -->
    <section class="max-w-screen-2xl mx-auto px-6 md:px-8 mb-24">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 lg:gap-8 mb-16">

            <!-- Passenger EV Card -->
            <a href="/products/saffire-smart-ride/" onclick="trackEvent('smart_ride_detail_click', {page_name: 'products'})" aria-label="View Saffire Smart Ride Details" class="group relative overflow-hidden bg-[#131315]/50 rounded-xl border border-primary/5 flex flex-col justify-end min-h-[500px] md:min-h-[600px] reveal-text block focus:outline-none focus:ring-2 focus:ring-primary">
                <div class="absolute top-6 left-6 z-20 flex flex-col gap-2">
                    <span class="inline-flex items-center px-3 py-1 bg-primary text-on-primary text-[10px] font-bold tracking-widest uppercase rounded-sm shadow-xl">D+3 Passenger Electric Vehicle</span>
                </div>
                
                <img loading="lazy" decoding="async" src="../images/SAFFIRE_PASSANGER.png" alt="Saffire Smart Ride" class="absolute inset-0 w-full h-full object-cover" />
                <div class="absolute inset-0 bg-gradient-to-t from-[#0e0e10] via-[#0e0e10]/70 to-transparent"></div>
                
                <div class="relative z-10 p-8 md:p-10">
                    <div class="flex flex-col gap-6">
                        <div>
                            <h3 class="font-headline text-3xl md:text-4xl font-bold mb-3 tracking-tight text-[#E5E1E4] group-hover:text-primary transition-colors">Saffire Smart Ride</h3>
                            <p class="font-body text-on-surface-variant max-w-sm font-light text-sm md:text-base leading-relaxed opacity-90">Saffire Smart Ride is a D+3 passenger electric three-wheeler designed for India’s evolving mobility needs, built for dependable daily passenger movement, driver-focused operation and efficient urban transport.</p>
                        </div>
                        
                        <div class="border-t border-primary/10 pt-6 mt-2">
                            <span class="inline-flex items-center gap-2 text-primary font-headline font-bold uppercase tracking-widest text-sm group-hover:brightness-125 transition-all">
                                View Smart Ride Details <span class="material-symbols-outlined text-[18px]">arrow_forward</span>
                            </span>
                        </div>
                    </div>
                </div>
            </a>

            <!-- Cargo EV Card -->
            <a href="/products/saffire-swiss-cargo/" onclick="trackEvent('swiss_cargo_detail_click', {page_name: 'products'})" aria-label="View Saffire Swiss Cargo Details" class="group relative overflow-hidden bg-[#131315]/50 rounded-xl border border-primary/5 flex flex-col justify-end min-h-[500px] md:min-h-[600px] reveal-text delay-100 block focus:outline-none focus:ring-2 focus:ring-primary">
                <div class="absolute top-6 left-6 z-20 flex flex-col gap-2">
                    <span class="inline-flex items-center px-3 py-1 bg-primary text-on-primary text-[10px] font-bold tracking-widest uppercase rounded-sm shadow-xl">Electric Cargo Loader</span>
                </div>
                
                <img loading="lazy" decoding="async" src="../images/saffire_loader.png" alt="Saffire Swiss Cargo" class="absolute inset-0 w-full h-full object-cover" />
                <div class="absolute inset-0 bg-gradient-to-t from-[#0e0e10] via-[#0e0e10]/70 to-transparent"></div>
                
                <div class="relative z-10 p-8 md:p-10">
                    <div class="flex flex-col gap-6">
                        <div>
                            <h3 class="font-headline text-3xl md:text-4xl font-bold mb-3 tracking-tight text-[#E5E1E4] group-hover:text-primary transition-colors">Saffire Swiss Cargo</h3>
                            <p class="font-body text-on-surface-variant max-w-sm font-light text-sm md:text-base leading-relaxed opacity-90">Saffire Swiss Cargo is an electric cargo loader engineered for last-mile logistics, business delivery and commercial load movement with strong payload capability and efficient electric performance.</p>
                        </div>
                        
                        <div class="border-t border-primary/10 pt-6 mt-2">
                            <span class="inline-flex items-center gap-2 text-primary font-headline font-bold uppercase tracking-widest text-sm group-hover:brightness-125 transition-all">
                                View Swiss Cargo Details <span class="material-symbols-outlined text-[18px]">arrow_forward</span>
                            </span>
                        </div>
                    </div>
                </div>
            </a>

        </div>

        <!-- Comparison Table -->
        <div class="bg-surface-container-low rounded-xl border border-outline-variant/10 overflow-hidden reveal-text">
            <div class="overflow-x-auto">
                <table class="w-full text-left min-w-[700px]">
                    <thead class="bg-surface-container-highest border-b border-outline-variant/20">
                        <tr>
                            <th class="py-4 px-6 font-label uppercase text-xs tracking-widest text-on-surface-variant w-1/4">Model</th>
                            <th class="py-4 px-6 font-label uppercase text-xs tracking-widest text-on-surface-variant">Category</th>
                            <th class="py-4 px-6 font-label uppercase text-xs tracking-widest text-on-surface-variant">Battery</th>
                            <th class="py-4 px-6 font-label uppercase text-xs tracking-widest text-on-surface-variant">Range</th>
                            <th class="py-4 px-6 font-label uppercase text-xs tracking-widest text-on-surface-variant">Payload</th>
                            <th class="py-4 px-6 font-label uppercase text-xs tracking-widest text-on-surface-variant">Top Speed</th>
                            <th class="py-4 px-6 font-label uppercase text-xs tracking-widest text-on-surface-variant">Wheelbase</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-outline-variant/10">
                        <tr class="hover:bg-[#131315]/50 transition-colors">
                            <td class="py-4 px-6 font-headline font-bold text-[#E5E1E4]">Saffire Smart Ride</td>
                            <td class="py-4 px-6 font-light text-on-surface-variant text-sm">D+3 Passenger</td>
                            <td class="py-4 px-6 font-light text-on-surface-variant text-sm">14.61 kWh / 63V 232Ah</td>
                            <td class="py-4 px-6 font-light text-on-surface-variant text-sm">200 km*</td>
                            <td class="py-4 px-6 font-light text-on-surface-variant text-sm">600 kg</td>
                            <td class="py-4 px-6 font-light text-on-surface-variant text-sm">50 km/hr</td>
                            <td class="py-4 px-6 font-light text-on-surface-variant text-sm">1948 mm</td>
                        </tr>
                        <tr class="hover:bg-[#131315]/50 transition-colors">
                            <td class="py-4 px-6 font-headline font-bold text-[#E5E1E4]">Saffire Swiss Cargo</td>
                            <td class="py-4 px-6 font-light text-on-surface-variant text-sm">Cargo Loader</td>
                            <td class="py-4 px-6 font-light text-on-surface-variant text-sm">14.61 kWh / 63V 232Ah</td>
                            <td class="py-4 px-6 font-light text-on-surface-variant text-sm">200 km*</td>
                            <td class="py-4 px-6 font-light text-on-surface-variant text-sm">600 kg</td>
                            <td class="py-4 px-6 font-light text-on-surface-variant text-sm">50 km/hr</td>
                            <td class="py-4 px-6 font-light text-on-surface-variant text-sm">2413 mm</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="p-4 bg-surface-container-lowest border-t border-outline-variant/10">
                <p class="text-xs font-light text-on-surface-variant italic">*Range and performance may vary based on load, route, driving conditions and temperature.</p>
            </div>
        </div>
    </section>

    <!-- Future Vehicles Roadmap -->"""

# We will use regex to find everything from <!-- Product Grid (Asymmetric Bento) --> or similar, up to <!-- Future Vehicles Roadmap -->
pattern = r'<!-- Product Grid.*?<!-- Future Vehicles Roadmap -->'
if re.search(pattern, content, flags=re.DOTALL):
    content = re.sub(pattern, new_section, content, flags=re.DOTALL)
else:
    print("Could not find the section to replace.")
    exit(1)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("products/index.html updated successfully.")
