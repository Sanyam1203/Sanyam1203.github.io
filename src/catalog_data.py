"""
Saffire EV - Central Catalog & Entity Data
Holds structured entity details, vehicle models, specifications,
regional dealership hubs, and commercial FAQs.
"""
from __future__ import annotations

from typing import Dict, List
from src.models import VehiclePlatform, TechnicalSpec, RegionalDealerHub, FAQItem

COMPANY_INFO = {
    "legal_name": "Koyo Gears India Private Limited",
    "brand_name": "Saffire EV",
    "short_brand": "Saffire",
    "parent_company": "Koyo Gears India Pvt. Ltd.",
    "legacy_brand": "Panther E-Rickshaw",
    "manufacturing_experience_years": "10+ Years (Since 2014)",
    "founding_year": 2014,
    "hq_address": "Plot 5, Om Tower, Mohkampur Phase 1, Delhi Road",
    "hq_city": "Meerut",
    "hq_state": "Uttar Pradesh",
    "hq_pincode": "250002",
    "hq_country": "India",
    "latitude": 28.9845,
    "longitude": 77.7064,
    "email": "inquiry@saffireev.com",
    "phone": "+91-92581-72967",
    "whatsapp": "+91-92581-72967",
    "whatsapp_link": "https://wa.me/919258172967",
    "website_url": "https://saffireev.com",
    "compliance": "ICAT Manesar Certified (AIS-040, AIS-053, AIS-156 Norms)",
    "cin": "U29253UP2013PTC059344",
    "alternate_names": [
        "Saffire EV",
        "Saffire Auto",
        "Saffire 3 Wheeler",
        "Saffire 3 Wheeler Auto",
        "Koyo Auto",
        "Koyo L5",
        "Koyo Gears India",
        "Koyo Gears India Private Limited",
        "Koyo Gears India Pvt Ltd",
        "Koyo Electric 3 Wheeler",
        "Saffire Electric Auto Rickshaw",
        "Saffire EV by Koyo Gears India"
    ],
    "knows_about": [
        "L5 Auto",
        "L5 Auto Rickshaw",
        "Electric Auto Rickshaw",
        "Auto Rickshaw",
        "KOYO Auto",
        "Koyo L5",
        "KOYO Gears India",
        "KOYO Electric 3 Wheeler",
        "Koyo Gears India Pvt Ltd",
        "Saffire Auto",
        "Saffire 3 Wheeler",
        "Saffire 3 Wheeler Auto",
        "Saffire EV",
        "Electric Cargo Loader",
        "Commercial EV Manufacturing",
        "ICAT Manesar Certified EVs"
    ],
    "brand_disambiguation_statement": "Saffire EV (encompassing Saffire Auto and Saffire 3 Wheeler) is the official commercial electric vehicle brand engineered and manufactured by Koyo Gears India Pvt. Ltd. (makers of Koyo Auto, Koyo L5, and Panther E-Rickshaw since 2014) headquartered in Meerut, Delhi NCR.",
    "social_links": {
        "linkedin": "https://www.linkedin.com/company/saffire-ev/",
        "facebook": "https://www.facebook.com/saffireev/",
        "instagram": "https://www.instagram.com/saffireev/"
    }
}

SMART_RIDE_SPECS: List[TechnicalSpec] = [
    TechnicalSpec(category="Powertrain & Battery", label="Battery Pack Capacity", value="14.61 kWh (63V 232Ah)", icon="battery_charging_full", highlight=True),
    TechnicalSpec(category="Powertrain & Battery", label="Peak Motor Power", value="6.3 kW (6300W) High-Torque PMSM", icon="electric_bolt", highlight=True),
    TechnicalSpec(category="Powertrain & Battery", label="Battery Chemistry", value="Advanced Lithium-Ion (NMC/LFP High Density)", icon="science"),
    TechnicalSpec(category="Powertrain & Battery", label="Charging Duration", value="5–6 Hours (Standard 16A Commercial Socket)", icon="schedule"),
    TechnicalSpec(category="Performance & Range", label="Certified Driving Range", value="200 km* per single charge", icon="route", highlight=True),
    TechnicalSpec(category="Performance & Range", label="Maximum Governed Speed", value="50 km/h (RTO Compliant L5 Category)", icon="speed", highlight=True),
    TechnicalSpec(category="Performance & Range", label="Gradability", value="15% (Handles steep flyovers & ramps loaded)", icon="landscape"),
    TechnicalSpec(category="Performance & Range", label="Running Cost", value="₹1.20 / km (vs ₹5.50 / km for Diesel Auto)", icon="savings", highlight=True),
    TechnicalSpec(category="Chassis & Dimensions", label="Seating Configuration", value="D+3 (Driver + 3 Passengers Ergonomic Seats)", icon="airline_seat_recline_normal", highlight=True),
    TechnicalSpec(category="Chassis & Dimensions", label="Wheelbase", value="1948 mm (High Stability & Legroom)", icon="straighten"),
    TechnicalSpec(category="Chassis & Dimensions", label="Rated Payload Capacity", value="600 kg Certified Commercial Payload", icon="weight", highlight=True),
    TechnicalSpec(category="Chassis & Dimensions", label="Tyre Specification", value="4.12-12 Rugged Tubeless Commercial Grade", icon="tire_repair"),
    TechnicalSpec(category="Safety & Compliance", label="Certification Agency", value="ICAT Manesar Tested & Approved", icon="verified"),
    TechnicalSpec(category="Safety & Compliance", label="Chassis Type", value="Heavy-Gauge Tubular High-Tensile Steel", icon="shield"),
    TechnicalSpec(category="Safety & Compliance", label="Braking System", value="Dual Circuit Hydraulic Drum Brakes with Park Lock", icon="sports_score"),
]

SWISS_CARGO_SPECS: List[TechnicalSpec] = [
    TechnicalSpec(category="Powertrain & Battery", label="Battery Pack Capacity", value="14.61 kWh (63V 232Ah)", icon="battery_charging_full", highlight=True),
    TechnicalSpec(category="Powertrain & Battery", label="Peak Motor Power", value="6.3 kW (6300W) High-Torque PMSM", icon="electric_bolt", highlight=True),
    TechnicalSpec(category="Powertrain & Battery", label="Battery Chemistry", value="Advanced Lithium-Ion (NMC/LFP High Density)", icon="science"),
    TechnicalSpec(category="Powertrain & Battery", label="Charging Duration", value="5–6 Hours (Standard 16A Commercial Socket)", icon="schedule"),
    TechnicalSpec(category="Performance & Range", label="Certified Driving Range", value="200 km* per single charge", icon="route", highlight=True),
    TechnicalSpec(category="Performance & Range", label="Maximum Governed Speed", value="50 km/h (RTO Compliant L5 Category)", icon="speed", highlight=True),
    TechnicalSpec(category="Performance & Range", label="Gradability", value="15% (Handles steep ramps with 600kg payload)", icon="landscape"),
    TechnicalSpec(category="Performance & Range", label="Running Cost", value="₹1.20 / km (Up to 78% operating cost reduction)", icon="savings", highlight=True),
    TechnicalSpec(category="Chassis & Dimensions", label="Vehicle Category", value="L5 Commercial Electric Cargo Loader (L5N)", icon="local_shipping", highlight=True),
    TechnicalSpec(category="Chassis & Dimensions", label="Wheelbase", value="2413 mm Long Wheelbase for High Stability", icon="straighten", highlight=True),
    TechnicalSpec(category="Chassis & Dimensions", label="Rated Payload Capacity", value="600 kg Certified Commercial Cargo Load", icon="weight", highlight=True),
    TechnicalSpec(category="Chassis & Dimensions", label="Tyre Specification", value="4.12-12 Heavy-Duty Commercial Cargo Tyres", icon="tire_repair"),
    TechnicalSpec(category="Safety & Compliance", label="Certification Agency", value="ICAT Manesar Tested & Approved", icon="verified"),
    TechnicalSpec(category="Safety & Compliance", label="Chassis Type", value="Reinforced High-Tensile Steel Cargo Deck", icon="shield"),
    TechnicalSpec(category="Safety & Compliance", label="Suspension", value="Heavy-Duty Multi-Leaf Springs with Hydraulic Dampers", icon="tune"),
]

VEHICLE_PLATFORMS: Dict[str, VehiclePlatform] = {
    "saffire-smart-ride": VehiclePlatform(
        id="saffire-smart-ride",
        name="Saffire Smart Ride",
        tagline="Next-Gen L5 Electric Passenger Auto Rickshaw",
        segment="L5 Electric Passenger Auto Rickshaw (D+3)",
        l5_category="L5M",
        url_path="/products/saffire-smart-ride/",
        battery_kwh=14.61,
        battery_spec="14.61 kWh (63V 232Ah) Advanced High-Capacity Lithium-ion",
        range_km=200,
        peak_power_kw=6.3,
        peak_power_spec="6.3 kW (6300W) High-Torque Heavy-Duty PMSM",
        top_speed_kmh=50,
        payload_kg=600,
        wheelbase_mm=1948,
        tyre_spec="4.12-12 Rugged Tubeless Commercial Grade",
        gradability_pct=15,
        charging_time_hrs="5–6 hours (Standard 16A Socket)",
        seating_capacity="D+3 (Driver + 3 Passengers with generous legroom)",
        cargo_volume=None,
        hero_image="/images/smart-ride-city.png",
        transparent_image="/images/SAFFIRE_PASSANGER.png",
        brochure_pdf="/assets/catalogs/saffire-ev-catalog.pdf",
        key_features=[
            "200 km* certified range per single charge eliminates midday charging halts",
            "14.61 kWh (63V 232Ah) high-density lithium-ion battery engineered for Indian thermal conditions",
            "6.3 kW peak power PMSM motor delivering instant low-end torque for quick city acceleration",
            "₹1.20/km operational cost saving up to ₹14,126 every month compared to diesel auto rickshaws",
            "D+3 ergonomic layout with 1948 mm wheelbase providing superior passenger comfort and legroom",
            "Full ICAT Manesar homologation and AIS safety compliance for fast RTO commercial registration"
        ],
        specs=SMART_RIDE_SPECS,
        description=(
            "The Saffire Smart Ride (colloquially known as Saffire Auto or Koyo L5) by Koyo Gears India Pvt. Ltd. "
            "is an ICAT-tested L5 passenger electric auto rickshaw engineered for urban transport, metro feeder routes, "
            "and inter-city passenger mobility. Powered by an advanced 14.61 kWh (63V 232Ah) lithium battery and a 6.3 kW peak "
            "powertrain, it delivers a certified 200 km range per charge, allowing commercial operators to achieve ₹14,000+ extra "
            "monthly earnings versus traditional diesel and CNG autos."
        ),
        meta_title="Saffire Smart Ride — L5 Auto Rickshaw & Electric 3 Wheeler Auto (D+3) | Koyo L5 by Saffire EV",
        meta_description="Official Saffire Smart Ride (Saffire Auto / Koyo L5) by Koyo Gears India: L5 Electric 3 Wheeler Auto Rickshaw (D+3). 200 km range, 14.61 kWh battery, 6.3 kW motor, 600 kg payload, ₹1.20/km cost.",
        h1_title="Saffire Smart Ride — L5 Auto Rickshaw & Electric 3 Wheeler Auto",
        alternate_names=[
            "Saffire Auto",
            "Saffire 3 Wheeler Auto",
            "Koyo Auto L5",
            "Koyo L5 Passenger Auto Rickshaw",
            "Saffire Smart Ride L5 Auto",
            "Koyo Electric 3 Wheeler",
            "L5 Auto Rickshaw"
        ],
        vehicle_configuration="L5 Category D+3 Electric Auto Rickshaw (3 Wheeler)"
    ),
    "saffire-swiss-cargo": VehiclePlatform(
        id="saffire-swiss-cargo",
        name="Saffire Swiss Cargo",
        tagline="Heavy-Duty 600 kg Payload L5 Electric Cargo Loader",
        segment="L5 Commercial Electric Cargo Loader",
        l5_category="L5N",
        url_path="/products/saffire-swiss-cargo/",
        battery_kwh=14.61,
        battery_spec="14.61 kWh (63V 232Ah) Industrial Grade Lithium-ion",
        range_km=200,
        peak_power_kw=6.3,
        peak_power_spec="6.3 kW (6300W) High-Torque PMSM Powertrain",
        top_speed_kmh=50,
        payload_kg=600,
        wheelbase_mm=2413,
        tyre_spec="4.12-12 Heavy-Duty Commercial Cargo Grade",
        gradability_pct=15,
        charging_time_hrs="5–6 hours (Standard 16A Socket)",
        seating_capacity=None,
        cargo_volume="Extra-Long Heavy-Gauge Cargo Bed with 2413 mm Wheelbase",
        hero_image="/images/swiss-cargo-delivery-route.png",
        transparent_image="/images/saffire_loader.png",
        brochure_pdf="/assets/catalogs/saffire-ev-catalog.pdf",
        key_features=[
            "600 kg certified payload capacity on reinforced high-tensile steel cargo deck",
            "2413 mm extended wheelbase ensuring roll stability and balanced axle load under full capacity",
            "14.61 kWh battery delivering 200 km* certified range for full-shift intra-city logistics",
            "6.3 kW high-torque motor effortlessly handles 15% inclines and flyover flyways when fully loaded",
            "₹1.20/km operating cost reduces delivery cost per package by up to 78% for logistics fleets",
            "ICAT Manesar certified commercial loader eligible for green commercial permit and bank financing"
        ],
        specs=SWISS_CARGO_SPECS,
        description=(
            "The Saffire Swiss Cargo (also recognized as Saffire 3 Wheeler Loader or Koyo L5 Cargo) by Koyo Gears India Pvt. Ltd. "
            "is an engineered L5 commercial electric cargo loader purpose-built for last-mile logistics, e-commerce distribution, "
            "industrial supply, and FMCG delivery. Featuring a rated 600 kg commercial payload, extended 2413 mm wheelbase, "
            "14.61 kWh lithium battery, and 6.3 kW peak motor, it slashes delivery running costs to just ₹1.20/km."
        ),
        meta_title="Saffire Swiss Cargo — L5 Electric 3 Wheeler Cargo Loader (600 kg) | Koyo Gears India",
        meta_description="Saffire Swiss Cargo by Koyo Gears India: Heavy-Duty L5 Electric 3 Wheeler Cargo Loader (Koyo L5 Cargo). 600 kg payload, 2413 mm wheelbase, 14.61 kWh battery, 200 km range, ₹1.20/km cost.",
        h1_title="Saffire Swiss Cargo — L5 Electric 3 Wheeler Cargo Loader",
        alternate_names=[
            "Saffire 3 Wheeler Cargo",
            "Koyo L5 Loader",
            "Koyo Electric 3 Wheeler Cargo",
            "Saffire Swiss Cargo L5",
            "Saffire Auto Loader",
            "L5 Cargo 3 Wheeler"
        ],
        vehicle_configuration="L5 Category Commercial Electric Cargo Loader (3 Wheeler)"
    )
}

REGIONAL_HUBS: List[RegionalDealerHub] = [
    RegionalDealerHub(
        city="Meerut",
        state="Uttar Pradesh",
        slug="meerut",
        hub_type="Corporate Headquarters & Primary Manufacturing Facility",
        address="Plot 5, Om Tower, Mohkampur Phase 1, Delhi Road",
        pincode="250002",
        latitude=28.9845,
        longitude=77.7064,
        phone="+91-92581-72967",
        email="inquiry@saffireev.com",
        operating_hours="Mon - Sat: 9:00 AM - 7:00 PM",
        is_headquarters=True
    ),
    RegionalDealerHub(
        city="Noida",
        state="Uttar Pradesh",
        slug="noida",
        hub_type="Delhi NCR Commercial Experience & Fleet Hub",
        address="Sector 63, Industrial Area, Noida",
        pincode="201301",
        latitude=28.6270,
        longitude=77.3750,
        phone="+91-92581-72967",
        email="inquiry@saffireev.com",
        operating_hours="Mon - Sat: 9:30 AM - 6:30 PM",
        is_headquarters=False
    ),
    RegionalDealerHub(
        city="Lucknow",
        state="Uttar Pradesh",
        slug="lucknow",
        hub_type="Central UP Regional Distribution & Service Hub",
        address="Transport Nagar, Kanpur Road, Lucknow",
        pincode="226012",
        latitude=26.7900,
        longitude=80.8900,
        phone="+91-92581-72967",
        email="inquiry@saffireev.com",
        operating_hours="Mon - Sat: 9:30 AM - 6:30 PM",
        is_headquarters=False
    ),
    RegionalDealerHub(
        city="Kanpur",
        state="Uttar Pradesh",
        slug="kanpur",
        hub_type="Industrial & Commercial Logistics Hub",
        address="Fazalganj Industrial Area, Kanpur",
        pincode="208012",
        latitude=26.4670,
        longitude=80.3150,
        phone="+91-92581-72967",
        email="inquiry@saffireev.com",
        operating_hours="Mon - Sat: 9:30 AM - 6:30 PM",
        is_headquarters=False
    ),
    RegionalDealerHub(
        city="Jaipur",
        state="Rajasthan",
        slug="jaipur",
        hub_type="Rajasthan Regional Sales & Dealership Center",
        address="VKIA Industrial Area, Sikar Road, Jaipur",
        pincode="302013",
        latitude=26.9600,
        longitude=75.7700,
        phone="+91-92581-72967",
        email="inquiry@saffireev.com",
        operating_hours="Mon - Sat: 9:30 AM - 6:30 PM",
        is_headquarters=False
    ),
    RegionalDealerHub(
        city="Delhi",
        state="Delhi",
        slug="delhi",
        hub_type="National Capital Territory Fleet Delivery Center",
        address="Mayapuri Industrial Area Phase II, New Delhi",
        pincode="110064",
        latitude=28.6300,
        longitude=77.1100,
        phone="+91-92581-72967",
        email="inquiry@saffireev.com",
        operating_hours="Mon - Sat: 9:00 AM - 7:00 PM",
        is_headquarters=False
    ),
    RegionalDealerHub(
        city="Patna",
        state="Bihar",
        slug="patna",
        hub_type="Eastern India Regional Service & Support Hub",
        address="Patliputra Industrial Area, Patna",
        pincode="800013",
        latitude=25.6200,
        longitude=85.1100,
        phone="+91-92581-72967",
        email="inquiry@saffireev.com",
        operating_hours="Mon - Sat: 9:30 AM - 6:30 PM",
        is_headquarters=False
    ),
    RegionalDealerHub(
        city="Agra",
        state="Uttar Pradesh",
        slug="agra",
        hub_type="Eco-Zone & Tourism Transport Experience Hub",
        address="Foundry Nagar, Hathras Road, Agra",
        pincode="282006",
        latitude=27.2000,
        longitude=78.0400,
        phone="+91-92581-72967",
        email="inquiry@saffireev.com",
        operating_hours="Mon - Sat: 9:30 AM - 6:30 PM",
        is_headquarters=False
    )
]

COMMERCIAL_FAQS: List[FAQItem] = [
    FAQItem(
        question="What is the real-world driving range of Saffire EV three-wheelers?",
        answer="Both the Saffire Smart Ride passenger auto and Saffire Swiss Cargo loader deliver a certified operating range of up to 200 km* on a single full charge under standard commercial driving conditions, powered by an advanced 14.61 kWh (63V 232Ah) lithium-ion battery.",
        category="Performance"
    ),
    FAQItem(
        question="Who manufactures Saffire EV vehicles and what is the engineering heritage?",
        answer="Saffire EV is engineered and manufactured by Koyo Gears India Pvt. Ltd. (CIN: U29253UP2013PTC059344), headquartered at Plot 5, Om Tower, Mohkampur Phase 1, Delhi Road, Meerut, UP. Koyo Gears India has over a decade of continuous EV manufacturing expertise since 2014, pioneering the popular Panther E-Rickshaw before expanding into heavy-duty L5 commercial platforms.",
        category="Company"
    ),
    FAQItem(
        question="How does Saffire EV compare to diesel and CNG auto rickshaws in running cost?",
        answer="Saffire EV operates at just ₹1.20 per km, compared to approximately ₹5.50 per km for diesel autos and ₹3.50 per km for CNG autos. An operator driving 100 km per day saves approximately ₹430 daily or ₹14,126 every month, translating to over ₹2,36,520 in cumulative savings over 5 years.",
        category="Economics"
    ),
    FAQItem(
        question="Are Saffire EV vehicles ICAT tested and approved for commercial RTO registration?",
        answer="Yes. Saffire EV platforms are fully tested, homologated, and approved by the International Centre for Automotive Technology (ICAT) Manesar in compliance with Central Motor Vehicle Rules (CMVR), AIS-040, AIS-053, and AIS-156 battery safety norms. They receive green commercial registration plates across all Indian states.",
        category="Compliance"
    ),
    FAQItem(
        question="What is the payload capacity of the Saffire Swiss Cargo loader?",
        answer="The Saffire Swiss Cargo features a certified commercial payload capacity of 600 kg. It is built on a heavy-gauge tubular chassis with an extended 2413 mm wheelbase and heavy-duty leaf springs to ensure roll stability under full commercial loading.",
        category="Specifications"
    ),
    FAQItem(
        question="What is the motor power and top speed of Saffire EV three-wheelers?",
        answer="Saffire EV platforms are powered by a 6.3 kW (6300W) peak power Permanent Magnet Synchronous Motor (PMSM) with high low-end torque. The top speed is governed at 50 km/h, providing safe, swift urban transit in compliance with Indian L5 commercial standards.",
        category="Specifications"
    ),
    FAQItem(
        question="How long does it take to charge the 14.61 kWh battery pack?",
        answer="A full recharge takes approximately 5 to 6 hours from a standard 16 Amp single-phase AC commercial wall socket, allowing drivers to recharge overnight at home or at standard depot charging points without requiring expensive proprietary DC fast chargers.",
        category="Charging"
    ),
    FAQItem(
        question="What is the difference between an L3 e-rickshaw and a Saffire L5 electric auto?",
        answer="L3 e-rickshaws are low-speed vehicles (restricted to 25 km/h, 1000W motor, light frames, short local trips). Saffire EV produces L5 vehicles—full commercial automotive grade with 50 km/h top speed, 6.3 kW peak PMSM motor, 14.61 kWh lithium battery, 200 km range, 600 kg payload, hydraulic brakes, and full CMVR compliance for highway and city artery transit.",
        category="Technical"
    ),
    FAQItem(
        question="Can Saffire EV vehicles navigate steep flyovers and ramps when loaded?",
        answer="Yes. Both Saffire platforms have a certified gradability rating of 15%, ensuring smooth starts and ascents on steep city flyovers, basement loading docks, and elevated bridges even under a full 600 kg commercial payload.",
        category="Performance"
    ),
    FAQItem(
        question="How do I apply for an authorized Saffire EV dealership or franchise?",
        answer="Prospective dealers can submit an application online through saffireev.com/ev-dealership-india/ or saffireev.com/contact/, email inquiry@saffireev.com, or WhatsApp +91-92581-72967. Saffire EV offers prime territorial exclusivity across 100+ cities in North and Central India.",
        category="Dealership"
    ),
    FAQItem(
        question="What investment and showroom space is required for a Saffire EV dealership?",
        answer="An authorized Saffire EV 3S (Sales, Service, Spare Parts) dealership typically requires an operational showroom space of 800 to 1,500 sq. ft. on a prominent commercial road, plus initial inventory working capital. Koyo Gears India provides complete layout design, technician training, and marketing support.",
        category="Dealership"
    ),
    FAQItem(
        question="Are commercial vehicle loans and bank financing options available?",
        answer="Yes. Because Saffire EV vehicles are ICAT Manesar homologated, they are approved for commercial vehicle asset financing by leading nationalized banks, private sector NBFCs, and state EV financing schemes with flexible EMI tenures of up to 3 to 5 years.",
        category="Finance"
    ),
    FAQItem(
        question="What warranty coverage is provided on the battery and powertrain?",
        answer="Saffire EV provides comprehensive manufacturer warranty coverage on the 14.61 kWh lithium-ion battery pack, PMSM electric motor, and electronic controller, backed by Koyo Gears India's nationwide service and spare parts network.",
        category="Warranty"
    ),
    FAQItem(
        question="Where can I see the vehicle in person or schedule a fleet test drive?",
        answer="You can visit the corporate headquarters and manufacturing facility at Mohkampur Industrial Area, Delhi Road, Meerut, or regional hubs in Noida, Lucknow, Kanpur, Jaipur, and Patna. Test drives can be booked through the Quick Query form on saffireev.com or via WhatsApp.",
        category="General"
    ),
    FAQItem(
        question="What tyre size is used on Saffire EV three-wheelers?",
        answer="Both platforms are fitted with 4.12-12 rugged commercial-grade tubeless tyres, engineered for superior grip, puncture resistance, and long tread life on Indian asphalt and rough secondary roads.",
        category="Specifications"
    ),
    FAQItem(
        question="Is the Saffire Smart Ride suitable for metro feeder and app-based auto aggregators?",
        answer="Yes. With D+3 seating, comfortable ergonomic seats, 1948 mm wheelbase, and 200 km range per charge, the Smart Ride is built specifically for high-duty city passenger transit, metro station connectivity, and ride-hailing fleets.",
        category="Applications"
    ),
    FAQItem(
        question="Can the Saffire Swiss Cargo bed be customized for specific fleet needs?",
        answer="Yes. The 2413 mm wheelbase chassis accommodates various container bodies including open-deck dropside cargo beds, closed delivery van boxes for e-commerce, refrigerated cold chain containers, and municipal waste collection tippers.",
        category="Applications"
    ),
    FAQItem(
        question="Does Saffire EV support FAME / EMPS / State EV subsidies?",
        answer="Saffire EV models comply with Central and State EV promotion policies, making buyers eligible for applicable state road tax exemptions, green registration fee waivers, and state capital EV incentives where active.",
        category="Compliance"
    ),
    FAQItem(
        question="How does Saffire EV ensure battery safety in hot Indian summers?",
        answer="The 14.61 kWh battery pack is engineered with an intelligent Battery Management System (BMS) that actively monitors individual cell voltages, temperature gradients, and current thresholds. It is housed in an IP67 water-and-dust proof aluminum enclosure compliant with AIS-156 Amendment 3 standards.",
        category="Safety"
    ),
    FAQItem(
        question="What is the wheelbase difference between the Smart Ride and Swiss Cargo?",
        answer="The Saffire Smart Ride passenger auto features a 1948 mm wheelbase optimized for passenger comfort and agile city manoeuvrability. The Saffire Swiss Cargo loader features an extended 2413 mm wheelbase to support a larger cargo bed and balanced weight distribution under 600 kg load.",
        category="Specifications"
    ),
    FAQItem(
        question="What maintenance does a Saffire EV require compared to a diesel auto?",
        answer="Unlike diesel autos that require regular engine oil changes, fuel filters, clutch plate replacements, and radiator flushes, Saffire EVs have no engine, no transmission gearbox, and no oil filters. Periodic maintenance is limited to tyre rotation, brake inspections, and suspension lubrication, reducing annual maintenance expenses by over 70%.",
        category="Maintenance"
    ),
    FAQItem(
        question="How can logistics companies integrate Saffire Swiss Cargo into their fleets?",
        answer="Logistics operators can pre-order fleet batches directly through saffireev.com/contact/ or inquiry@saffireev.com. Saffire EV provides telematics-ready vehicle architectures, dedicated fleet bulk pricing, and centralized spare part replenishment agreements.",
        category="Fleet"
    ),
    FAQItem(
        question="Can drivers charge Saffire EVs at public charging stations?",
        answer="Yes. Saffire EV can be charged at any commercial or public charging station equipped with standard 16A AC charging points, in addition to home wall-socket charging.",
        category="Charging"
    ),
    FAQItem(
        question="What braking system is fitted on Saffire EV vehicles?",
        answer="Saffire EVs feature a dual-circuit hydraulic drum braking system with independent mechanical parking brakes, engineered to safely stop a fully loaded 600 kg commercial payload with short stopping distances.",
        category="Safety"
    ),
    FAQItem(
        question="How do I get an on-road price quote in my city?",
        answer="Click the 'Quick Query / On-Road Price' button on saffireev.com, select your city and required model (Smart Ride or Swiss Cargo), and our regional sales team will provide an official on-road quotation including state taxes, insurance, and available financing offers within 2 hours.",
        category="Purchase"
    )
]

