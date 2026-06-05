import csv
import os
import random
import urllib.parse
from datetime import datetime, timedelta

# Configuration
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'datasets')
os.makedirs(OUTPUT_DIR, exist_ok=True)
PRODUCTS_CSV = os.path.join(OUTPUT_DIR, 'products.csv')
INTERACTIONS_CSV = os.path.join(OUTPUT_DIR, 'interactions.csv')

# Base Catalog
CATALOG = {
    "Electronics": [
        [
            "Sony",
            "WH-1000XM5 Wireless Headphones",
            398.0,
            "Industry leading noise canceling with two processors and 8 microphones for unprecedented listening quality.",
            "https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?auto=format&fit=crop&q=80&w=600",
            [
                "Black",
                "Silver",
                "Midnight Blue"
            ]
        ],
        [
            "Samsung",
            "55-Inch Class QLED 4K Smart TV",
            797.99,
            "Experience the power of QLED. Dual LED backlighting provides enhanced contrast.",
            "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?auto=format&fit=crop&q=80&w=600",
            [
                "55-Inch",
                "65-Inch"
            ]
        ],
        [
            "Apple",
            "MacBook Air M2",
            1199.0,
            "Supercharged by M2. Incredibly thin and light laptop with a 13.6-inch Liquid Retina display.",
            "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?auto=format&fit=crop&q=80&w=600",
            [
                "Midnight",
                "Starlight",
                "Space Gray",
                "Silver"
            ]
        ],
        [
            "JBL",
            "Tune 230NC TWS True Wireless Earbuds",
            99.95,
            "Active noise cancelling with smart ambient. Up to 40 hours of battery life.",
            "https://images.unsplash.com/photo-1606220588913-b3aea9ebb173?auto=format&fit=crop&q=80&w=600",
            [
                "Black",
                "White",
                "Blue"
            ]
        ],
        [
            "Bose",
            "SoundLink Micro Bluetooth Speaker",
            119.0,
            "Small portable speaker with surprisingly big sound and deep bass. Waterproof design.",
            "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&q=80&w=600",
            [
                "Black",
                "Stone Blue",
                "White Smoke"
            ]
        ],
        [
            "Garmin",
            "Venu 2 Fitness Smartwatch",
            399.99,
            "Advanced health monitoring and fitness features to help you better understand what's going on inside your body.",
            "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?auto=format&fit=crop&q=80&w=600",
            [
                "Granite Blue",
                "Black",
                "Silver"
            ]
        ],
        [
            "Apple",
            "iPad Pro 11-inch (M2)",
            799.0,
            "Astonishing performance, incredibly advanced displays, superfast wireless connectivity, and next-level Apple Pencil capabilities.",
            "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?auto=format&fit=crop&q=80&w=600",
            [
                "Space Gray",
                "Silver"
            ]
        ],
        [
            "Canon",
            "EOS R6 Full-Frame Mirrorless Camera",
            2499.0,
            "20 Megapixel full-frame CMOS sensor, DIGIC X image processor, and 4K up to 60fps video.",
            "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&q=80&w=600",
            [
                "Body Only",
                "With 24-105mm Lens"
            ]
        ],
        [
            "Logitech",
            "G Pro X Mechanical Gaming Keyboard",
            129.99,
            "Pro-grade mechanical keyboard built for esports athletes with swappable switches.",
            "https://images.unsplash.com/photo-1605445207797-200a747cf995?auto=format&fit=crop&q=80&w=600",
            [
                "Linear",
                "Tactile",
                "Clicky"
            ]
        ],
        [
            "Razer",
            "DeathAdder V2 Gaming Mouse",
            69.99,
            "Wired gaming mouse with 20K DPI optical sensor and fastest gaming mouse switch.",
            "https://images.unsplash.com/photo-1628173549725-3b978fc964b7?auto=format&fit=crop&q=80&w=600",
            [
                "Classic Black",
                "Halo Edition"
            ]
        ],
        [
            "Anker",
            "PowerCore 20,000mAh Power Bank",
            49.99,
            "Ultra-high capacity portable charger with dual USB ports and fast charging technology.",
            "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?auto=format&fit=crop&q=80&w=600",
            [
                "Black",
                "White"
            ]
        ],
        [
            "Logitech",
            "C920x HD Pro Webcam",
            69.99,
            "Full HD 1080p video calling and recording, dual microphones for clear stereo audio.",
            "https://images.unsplash.com/photo-1587826080692-f439cd0b70da?auto=format&fit=crop&q=80&w=600",
            [
                "Black"
            ]
        ],
        [
            "Samsung",
            "T7 Shield 1TB Portable SSD",
            119.99,
            "Rugged, fast, and compact portable solid state drive for creators on the go.",
            "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?auto=format&fit=crop&q=80&w=600",
            [
                "Black",
                "Blue",
                "Beige"
            ]
        ],
        [
            "Apple",
            "AirPods Pro (2nd Gen)",
            249.0,
            "Richer audio experience, up to 2x more Active Noise Cancellation, and Adaptive Transparency.",
            "https://images.unsplash.com/photo-1583394838336-acd977736f90?auto=format&fit=crop&q=80&w=600",
            [
                "Standard"
            ]
        ],
        [
            "Amazon",
            "Echo Dot (5th Gen)",
            49.99,
            "Our best-sounding Echo Dot yet. Enjoy an improved audio experience and smart home hub.",
            "https://images.unsplash.com/photo-1543512214-318228f60fc0?auto=format&fit=crop&q=80&w=600",
            [
                "Charcoal",
                "Glacier White",
                "Deep Sea Blue"
            ]
        ]
    ],
    "Clothing": [
        [
            "Levi's",
            "Men's 501 Original Fit Jeans",
            59.5,
            "The original blue jean since 1873. A blank canvas for self-expression with a classic straight fit.",
            "https://images.unsplash.com/photo-1542272604-787c3835535d?auto=format&fit=crop&q=80&w=600",
            [
                "Dark Stonewash",
                "Light Blue",
                "Black"
            ]
        ],
        [
            "Champion",
            "Reverse Weave Pullover Hoodie",
            65.0,
            "Heavyweight fleece hoodie designed to resist vertical shrinkage and offer a classic athletic fit.",
            "https://images.unsplash.com/photo-1556821840-3a63f95609a7?auto=format&fit=crop&q=80&w=600",
            [
                "Oxford Grey",
                "Black",
                "Navy"
            ]
        ],
        [
            "Adidas",
            "Tiro 21 Track Jacket",
            50.0,
            "Classic soccer-inspired track jacket featuring moisture-absorbing AEROREADY fabric.",
            "https://images.unsplash.com/photo-1591047139829-d9d13e3bc891?auto=format&fit=crop&q=80&w=600",
            [
                "Black/White",
                "Team Navy",
                "Red"
            ]
        ],
        [
            "Carhartt",
            "Loose Fit Heavyweight Cotton T-Shirt",
            19.99,
            "Durable, comfortable, and built for work. This classic pocket tee has a relaxed fit.",
            "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&q=80&w=600",
            [
                "Black",
                "Heather Grey",
                "Navy",
                "Desert"
            ]
        ],
        [
            "Dockers",
            "Classic Fit Easy Khaki Pants",
            39.99,
            "The classic khaki pant with stretch for performance and easy care wrinkle resistance.",
            "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?auto=format&fit=crop&q=80&w=600",
            [
                "British Khaki",
                "Black",
                "Navy"
            ]
        ],
        [
            "Under Armour",
            "Tech 2.0 Short Sleeve Polo",
            39.99,
            "Textured fabric that's soft, light & breathable for maximum active comfort.",
            "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?auto=format&fit=crop&q=80&w=600",
            [
                "Academy Blue",
                "Black",
                "White",
                "Graphite"
            ]
        ],
        [
            "Patagonia",
            "Better Sweater 1/4 Zip Fleece",
            139.0,
            "A warm, low-bulk quarter-zip pullover made of soft, sweater-knit recycled polyester fleece.",
            "https://images.unsplash.com/photo-1617326857907-7e04918e6922?auto=format&fit=crop&q=80&w=600",
            [
                "Stonewash",
                "Black",
                "Navy Blue"
            ]
        ],
        [
            "Ralph Lauren",
            "Classic Fit Oxford Shirt",
            115.0,
            "A pillar of the Polo style, featuring signature pony embroidery and a classic button-down collar.",
            "https://images.unsplash.com/photo-1598033129183-c4f50c736c10?auto=format&fit=crop&q=80&w=600",
            [
                "White",
                "Light Blue",
                "Pink"
            ]
        ],
        [
            "Nike",
            "Sportswear Club Fleece Joggers",
            55.0,
            "Classic comfort meets street style. Soft fleece with a classic relaxed jogger fit.",
            "https://images.unsplash.com/photo-1552902865-b72c031ac5ea?auto=format&fit=crop&q=80&w=600",
            [
                "Black",
                "Dark Grey Heather",
                "Midnight Navy"
            ]
        ],
        [
            "The North Face",
            "Aconcagua 2 Puffer Jacket",
            185.0,
            "Insulated puffer jacket combining natural down and synthetic insulation for reliable warmth.",
            "https://images.unsplash.com/photo-1551028719-00167b16eac5?auto=format&fit=crop&q=80&w=600",
            [
                "TNF Black",
                "Navy",
                "Olive"
            ]
        ],
        [
            "Levi's",
            "Type III Sherpa Lined Denim Trucker",
            98.0,
            "The original jean jacket upgraded with a warm sherpa lining and collar.",
            "https://images.unsplash.com/photo-1576871337632-b9aef4c17ab9?auto=format&fit=crop&q=80&w=600",
            [
                "Mustard",
                "Black",
                "Vintage Wash"
            ]
        ],
        [
            "L.L.Bean",
            "Scotch Plaid Flannel Shirt",
            54.95,
            "Authentic Scottish tartan plaid crafted from exceptionally soft, durable Portuguese cotton.",
            "https://images.unsplash.com/photo-1601379329542-31c59347e2b8?auto=format&fit=crop&q=80&w=600",
            [
                "Dress Gordon",
                "Black Watch",
                "Rob Roy"
            ]
        ],
        [
            "Columbia",
            "Watertight II Rain Jacket",
            75.0,
            "Lightweight, waterproof, and breathable rain jacket that packs into its own pocket.",
            "https://images.unsplash.com/photo-1545594861-3bef43ff2fc8?auto=format&fit=crop&q=80&w=600",
            [
                "Black",
                "Graphite",
                "Navy"
            ]
        ],
        [
            "Calvin Klein",
            "Cotton Classics V-Neck T-Shirts (3-Pack)",
            39.5,
            "Soft, breathable cotton v-neck undershirts for everyday comfort and layering.",
            "https://images.unsplash.com/photo-1581655353564-df123a1eb820?auto=format&fit=crop&q=80&w=600",
            [
                "White",
                "Black"
            ]
        ],
        [
            "Tommy Hilfiger",
            "Cotton Cable Knit Sweater",
            69.5,
            "Classic cable-knit sweater with signature flag logo embroidery on the chest.",
            "https://images.unsplash.com/photo-1543076447-215ad9ba6923?auto=format&fit=crop&q=80&w=600",
            [
                "Ivory",
                "Navy",
                "Grey Heather"
            ]
        ]
    ],
    "Shoes": [
        [
            "Nike",
            "Air Force 1 '07",
            115.0,
            "The radiance lives on in the Nike Air Force 1 \u201907, the b-ball icon that puts a fresh spin on what you know best.",
            "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?auto=format&fit=crop&q=80&w=600",
            [
                "White/White",
                "Black/Black"
            ]
        ],
        [
            "Adidas",
            "Ultraboost 1.0",
            190.0,
            "Iconic running shoes with responsive BOOST midsole for incredible energy return.",
            "https://images.unsplash.com/photo-1608231387042-66d1773070a5?auto=format&fit=crop&q=80&w=600",
            [
                "Core Black",
                "Cloud White",
                "Grey"
            ]
        ],
        [
            "Converse",
            "Chuck Taylor All Star High Top",
            65.0,
            "The unmistakable classic canvas sneaker with star-centered ankle patch.",
            "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?auto=format&fit=crop&q=80&w=600",
            [
                "Optical White",
                "Black",
                "Navy"
            ]
        ],
        [
            "Nike",
            "Air Jordan 1 Mid",
            125.0,
            "Inspired by the original AJ1, this mid-top edition maintains the iconic look you love.",
            "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&q=80&w=600",
            [
                "Chicago",
                "Bred",
                "Shadow"
            ]
        ],
        [
            "Salomon",
            "Speedcross 6 Trail Running Shoe",
            140.0,
            "Legendary trail running shoe featuring deep, sharp lugs for unmatched grip on mud.",
            "https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?auto=format&fit=crop&q=80&w=600",
            [
                "Black/Black",
                "Sulphur/Black"
            ]
        ],
        [
            "Cole Haan",
            "Grand Crosscourt Sneaker",
            150.0,
            "A classic court sneaker refined in premium leather with incredibly lightweight cushioning.",
            "https://images.unsplash.com/photo-1614252369475-531eba835eb1?auto=format&fit=crop&q=80&w=600",
            [
                "White Leather",
                "British Tan",
                "Navy"
            ]
        ],
        [
            "Timberland",
            "6-Inch Premium Waterproof Boot",
            210.0,
            "The original Timberland boot built with premium waterproof leather and seam-sealed construction.",
            "https://images.unsplash.com/photo-1520639888713-7851133b1ed0?auto=format&fit=crop&q=80&w=600",
            [
                "Wheat Nubuck",
                "Black Nubuck"
            ]
        ],
        [
            "New Balance",
            "574 Core Sneaker",
            89.99,
            "A timeless retro silhouette with lightweight EVA foam cushioning for everyday wear.",
            "https://images.unsplash.com/photo-1608064910359-e374d642facc?auto=format&fit=crop&q=80&w=600",
            [
                "Grey/White",
                "Navy/White",
                "Black/White"
            ]
        ],
        [
            "ASICS",
            "GEL-Kayano 30 Running Shoe",
            160.0,
            "Advanced stability and soft cushioning properties for distance running.",
            "https://images.unsplash.com/photo-1539185441755-769473a23570?auto=format&fit=crop&q=80&w=600",
            [
                "Black/White",
                "French Blue"
            ]
        ],
        [
            "Dr. Martens",
            "2976 Smooth Leather Chelsea Boots",
            170.0,
            "Classic Chelsea boot styling built on the iconic and comfortable Dr. Martens air-cushioned sole.",
            "https://images.unsplash.com/photo-1638247025967-b4e38f787b76?auto=format&fit=crop&q=80&w=600",
            [
                "Black Smooth",
                "Cherry Red Smooth"
            ]
        ],
        [
            "Vans",
            "Old Skool Classic Skate Shoe",
            70.0,
            "The classic Vans skate shoe featuring the iconic side stripe, low top lace-up, and waffle rubber outsoles.",
            "https://images.unsplash.com/photo-1491553895911-0055eca6402d?auto=format&fit=crop&q=80&w=600",
            [
                "Black/White",
                "Navy",
                "Checkerboard"
            ]
        ],
        [
            "Under Armour",
            "Project Rock 6 Training Shoe",
            150.0,
            "Durable, stable training shoe engineered for heavy lifting and intense workouts.",
            "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?auto=format&fit=crop&q=80&w=600",
            [
                "Black/Grey",
                "White/Black"
            ]
        ],
        [
            "Skechers",
            "GO WALK 6 Walking Shoe",
            65.0,
            "Features lightweight, responsive ULTRA GO cushioning and high-rebound Comfort Pillar Technology.",
            "https://images.unsplash.com/photo-1588361861040-ac9b1018f6d5?auto=format&fit=crop&q=80&w=600",
            [
                "Black",
                "Navy",
                "Charcoal"
            ]
        ],
        [
            "Reebok",
            "Club C 85 Vintage Sneakers",
            90.0,
            "Clean, minimalist tennis-inspired style crafted with a soft garment leather upper.",
            "https://images.unsplash.com/photo-1511556820780-d912e42b4980?auto=format&fit=crop&q=80&w=600",
            [
                "Chalk/Paperwhite",
                "White/Navy"
            ]
        ],
        [
            "Teva",
            "Hurricane XLT2 Sport Sandal",
            75.0,
            "Rugged outdoor sandal with adjustable straps and durable rubber traction outsoles.",
            "https://images.unsplash.com/photo-1562183241-b937e95585b6?auto=format&fit=crop&q=80&w=600",
            [
                "Black",
                "Olive",
                "Navy"
            ]
        ]
    ],
    "Accessories": [
        [
            "Ray-Ban",
            "Original Wayfarer Classic Sunglasses",
            163.0,
            "The most recognizable style in the history of sunglasses. Classic G-15 lenses.",
            "https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&q=80&w=600",
            [
                "Black/Green",
                "Tortoise/Brown"
            ]
        ],
        [
            "Casio",
            "G-Shock Classic Digital Watch",
            49.95,
            "Shock resistant, 200M water resistant, and EL backlight with Afterglow.",
            "https://images.unsplash.com/photo-1596541617260-1533ad3bcf07?auto=format&fit=crop&q=80&w=600",
            [
                "Black",
                "Olive Green"
            ]
        ],
        [
            "Bellroy",
            "Hide & Seek Leather Wallet",
            89.0,
            "A traditional looking bifold with hidden features and RFID protection.",
            "https://images.unsplash.com/photo-1627123424574-724758594e93?auto=format&fit=crop&q=80&w=600",
            [
                "Java",
                "Black",
                "Caramel"
            ]
        ],
        [
            "Herschel",
            "Little America Backpack",
            109.99,
            "A popular mountaineering silhouette featuring a padded/fleece lined 15-inch laptop sleeve.",
            "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&q=80&w=600",
            [
                "Black",
                "Navy",
                "Raven Crosshatch"
            ]
        ],
        [
            "Seiko",
            "Prospex Automatic Diver's Watch",
            450.0,
            "A professional diver's watch with an automatic movement and durable stainless steel case.",
            "https://images.unsplash.com/photo-1524805444758-089113d48a6d?auto=format&fit=crop&q=80&w=600",
            [
                "Silver/Black",
                "Silver/Blue"
            ]
        ],
        [
            "Oakley",
            "Holbrook Square Sunglasses",
            154.0,
            "A timeless, classic design fused with modern Oakley technology. Prizm lenses included.",
            "https://images.unsplash.com/photo-1559564177-d0c3c8f8d689?auto=format&fit=crop&q=80&w=600",
            [
                "Matte Black",
                "Woodgrain"
            ]
        ],
        [
            "Fossil",
            "Derrick RFID Bifold Wallet",
            45.0,
            "Classic 100% genuine leather bifold wallet with RFID blocking technology.",
            "https://images.unsplash.com/photo-1606503153255-59d8b8b82176?auto=format&fit=crop&q=80&w=600",
            [
                "Dark Brown",
                "Black"
            ]
        ],
        [
            "Patagonia",
            "Black Hole Duffel 55L",
            159.0,
            "A highly weather-resistant and rugged duffel bag that easily carries your gear.",
            "https://images.unsplash.com/photo-1550418290-a8d86ad674a6?auto=format&fit=crop&q=80&w=600",
            [
                "Black",
                "Smolder Blue",
                "Red"
            ]
        ],
        [
            "Tissot",
            "PRX Powermatic 80 Watch",
            725.0,
            "Evoking an authentic 1970s aesthetic. Automatic movement with up to 80 hours power reserve.",
            "https://images.unsplash.com/photo-1622329618074-d4b9981ed73e?auto=format&fit=crop&q=80&w=600",
            [
                "Stainless Steel/Blue",
                "Stainless Steel/Black"
            ]
        ],
        [
            "Oakley",
            "Radar EV Path Sport Sunglasses",
            211.0,
            "Extended range of view in the upper peripheral region. Perfect for cycling and running.",
            "https://images.unsplash.com/photo-1572635196237-14b3f281503f?auto=format&fit=crop&q=80&w=600",
            [
                "Matte Black/Prizm Road",
                "White/Prizm Sapphire"
            ]
        ],
        [
            "Timberland",
            "Classic Leather Jean Belt",
            24.99,
            "A 100% genuine leather heavy duty belt designed for jeans or casual wear.",
            "https://images.unsplash.com/photo-1603808033192-082d6919d3e1?auto=format&fit=crop&q=80&w=600",
            [
                "Brown",
                "Black",
                "Wheat"
            ]
        ],
        [
            "Timbuk2",
            "Classic Messenger Bag",
            99.0,
            "The original messenger bag designed in San Francisco. Waterproof TPU liner.",
            "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?auto=format&fit=crop&q=80&w=600",
            [
                "Jet Black",
                "Eco Gunmetal",
                "Navy"
            ]
        ],
        [
            "Hamilton",
            "Khaki Field Mechanical Watch",
            595.0,
            "Rugged and robust 38mm field watch featuring a hand-wound mechanical movement.",
            "https://images.unsplash.com/photo-1549972352-7104fded7a30?auto=format&fit=crop&q=80&w=600",
            [
                "Olive Drab NATO",
                "Brown Leather"
            ]
        ],
        [
            "Carhartt",
            "Trade Series Crossbody Bag",
            29.99,
            "Durable, water-repellent crossbody bag perfect for keeping daily essentials close.",
            "https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&q=80&w=600",
            [
                "Carhartt Brown",
                "Black",
                "Navy"
            ]
        ],
        [
            "New Era",
            "59FIFTY Fitted Baseball Cap",
            41.99,
            "The authentic fitted cap worn by MLB players on the field. Flat bill and high crown.",
            "https://images.unsplash.com/photo-1588850561407-ed78c334e67a?auto=format&fit=crop&q=80&w=600",
            [
                "NY Yankees Navy",
                "LA Dodgers Blue"
            ]
        ]
    ],
    "Home & Kitchen": [
        [
            "Instant Pot",
            "Duo 7-in-1 Pressure Cooker (6 Qt)",
            99.99,
            "Multi-cooker that replaces 7 appliances: pressure cooker, slow cooker, rice cooker, steamer, saut\u00e9 pan, yogurt maker.",
            "https://images.unsplash.com/photo-1585515320310-259814833e62?auto=format&fit=crop&q=80&w=600",
            [
                "Stainless Steel/Black"
            ]
        ],
        [
            "iRobot",
            "Roomba i4+ EVO Robot Vacuum",
            399.99,
            "Self-emptying robot vacuum that learns your home and cleans by room.",
            "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?auto=format&fit=crop&q=80&w=600",
            [
                "Grey"
            ]
        ],
        [
            "KitchenAid",
            "Artisan Series 5-Quart Stand Mixer",
            449.99,
            "Iconic stand mixer with tilt-head design and 10 speeds. Includes 5-quart stainless steel bowl.",
            "https://images.unsplash.com/photo-1594385208974-2f8bb07ecc07?auto=format&fit=crop&q=80&w=600",
            [
                "Empire Red",
                "Onyx Black",
                "Aqua Sky"
            ]
        ],
        [
            "Keurig",
            "K-Elite Single Serve Coffee Maker",
            149.99,
            "Brews multiple K-Cup pod sizes and includes an iced setting for full-flavored iced coffee.",
            "https://images.unsplash.com/photo-1517701550927-30cf4ba1dba5?auto=format&fit=crop&q=80&w=600",
            [
                "Brushed Slate",
                "Silver",
                "Black"
            ]
        ],
        [
            "Dyson",
            "V8 Absolute Cordless Vacuum",
            469.99,
            "Powerful, lightweight cordless vacuum engineered for homes with pets.",
            "https://images.unsplash.com/photo-1558317374-067fb5f30001?auto=format&fit=crop&q=80&w=600",
            [
                "Nickel/Yellow",
                "Iron/Red"
            ]
        ],
        [
            "Ninja",
            "Air Fryer Max XL (5.5 Qt)",
            129.99,
            "Fast, crispy, and evenly cooked food with up to 75% less fat than traditional frying.",
            "https://images.unsplash.com/photo-1648733413009-ff0e203f6488?auto=format&fit=crop&q=80&w=600",
            [
                "Grey/Black"
            ]
        ],
        [
            "Brita",
            "Everyday 10-Cup Water Filter Pitcher",
            29.99,
            "Reduces chlorine, copper, mercury, and cadmium impurities found in tap water.",
            "https://images.unsplash.com/photo-1602143407151-7111542de6e8?auto=format&fit=crop&q=80&w=600",
            [
                "White",
                "Black"
            ]
        ],
        [
            "Cuisinart",
            "11-Piece Stainless Steel Cookware Set",
            199.0,
            "Professional-grade stainless steel cookware set providing optimal heat distribution.",
            "https://images.unsplash.com/photo-1556909114-44e3e70034e2?auto=format&fit=crop&q=80&w=600",
            [
                "Stainless Steel"
            ]
        ],
        [
            "Breville",
            "Barista Express Espresso Machine",
            699.95,
            "Create great tasting espresso in less than a minute with a built-in conical burr grinder.",
            "https://images.unsplash.com/photo-1610889556528-9a770e32642f?auto=format&fit=crop&q=80&w=600",
            [
                "Brushed Stainless Steel",
                "Black Sesame"
            ]
        ],
        [
            "Lodge",
            "12-Inch Cast Iron Skillet",
            29.95,
            "Pre-seasoned cast iron skillet for unparalleled heat retention and even heating.",
            "https://images.unsplash.com/photo-1626074353765-517a681e40be?auto=format&fit=crop&q=80&w=600",
            [
                "Cast Iron Black"
            ]
        ],
        [
            "Levoit",
            "Core 300 True HEPA Air Purifier",
            99.99,
            "High-efficiency air purifier removing 99.97% of airborne particles 0.3 microns in size.",
            "https://images.unsplash.com/photo-1585771724684-38269d6639fd?auto=format&fit=crop&q=80&w=600",
            [
                "White",
                "Black"
            ]
        ],
        [
            "Vitamix",
            "E310 Explorian Blender",
            349.95,
            "Professional-grade blender with variable speed control and pulse feature.",
            "https://images.unsplash.com/photo-1570222094714-4281f1aa910d?auto=format&fit=crop&q=80&w=600",
            [
                "Slate",
                "Black",
                "Red"
            ]
        ],
        [
            "Fellow",
            "Stagg EKG Electric Pour-Over Kettle",
            165.0,
            "Variable temperature control kettle with a precision pour spout.",
            "https://images.unsplash.com/photo-1556909172-54557c7e4fb7?auto=format&fit=crop&q=80&w=600",
            [
                "Matte Black",
                "Matte White",
                "Copper"
            ]
        ],
        [
            "Breville",
            "Smart Oven Pro Convection Toaster",
            279.95,
            "Convection powered countertop oven with Element IQ system for smart heat distribution.",
            "https://images.unsplash.com/photo-1574269909862-7e1d70bb8078?auto=format&fit=crop&q=80&w=600",
            [
                "Brushed Stainless Steel"
            ]
        ],
        [
            "Simplehuman",
            "Steel Frame Dish Rack",
            89.99,
            "Premium stainless steel dish rack with an innovative drainage system.",
            "https://images.unsplash.com/photo-1556909190-6a1a4e72be4b?auto=format&fit=crop&q=80&w=600",
            [
                "Fingerprint-Proof Stainless Steel"
            ]
        ]
    ],
    "Sports & Outdoors": [
        [
            "Hydro Flask",
            "Wide Mouth Insulated Water Bottle (32 oz)",
            44.95,
            "TempShield insulation eliminates condensation and keeps beverages cold up to 24 hours.",
            "https://images.unsplash.com/photo-1544186595-df6110f01a34?auto=format&fit=crop&q=80&w=600",
            [
                "Black",
                "Pacific Blue",
                "Olive"
            ]
        ],
        [
            "Lululemon",
            "The Reversible Mat 5mm",
            88.0,
            "A polyurethane top layer absorbs moisture to help you get a grip during sweaty practices.",
            "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?auto=format&fit=crop&q=80&w=600",
            [
                "Black/White",
                "True Navy"
            ]
        ],
        [
            "Gritin",
            "Resistance Bands Set of 5",
            14.99,
            "Skin-friendly natural latex resistance bands for yoga, pilates, and home workouts.",
            "https://images.unsplash.com/photo-1598289431512-b97b0917affc?auto=format&fit=crop&q=80&w=600",
            [
                "Multicolor Set"
            ]
        ],
        [
            "Coleman",
            "Sundome 2-Person Camping Tent",
            69.99,
            "WeatherTec system features patented welded floors and inverted seams to keep water out.",
            "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&q=80&w=600",
            [
                "Green/Grey",
                "Navy/Grey"
            ]
        ],
        [
            "Bowflex",
            "SelectTech 552 Adjustable Dumbbells (Pair)",
            429.0,
            "Adjusts from 5 to 52.5 lbs in 2.5 lb increments to replace 15 sets of weights.",
            "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&q=80&w=600",
            [
                "Black/Red"
            ]
        ],
        [
            "Garmin",
            "Forerunner 255 GPS Running Watch",
            349.99,
            "Advanced running metrics, training load insights, and daily suggested workouts.",
            "https://images.unsplash.com/photo-1510017803350-1a824394ff56?auto=format&fit=crop&q=80&w=600",
            [
                "Tidal Blue",
                "Slate Grey"
            ]
        ],
        [
            "Osprey",
            "Daylite Plus Daypack",
            75.0,
            "Versatile daypack featuring a padded laptop/hydration sleeve and dual mesh side pockets.",
            "https://images.unsplash.com/photo-1501554728187-ce583db33af7?auto=format&fit=crop&q=80&w=600",
            [
                "Black",
                "Night Shift Blue",
                "Wave Blue"
            ]
        ],
        [
            "TriggerPoint",
            "GRID Foam Roller",
            36.99,
            "Patented GRID design features multi-density exterior to channel blood and oxygen to muscle tissue.",
            "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&q=80&w=600",
            [
                "Orange",
                "Black",
                "Pink"
            ]
        ],
        [
            "YETI",
            "Tundra 45 Hard Cooler",
            325.0,
            "FatWall design holds up to two inches of insulation for unmatched ice retention.",
            "https://images.unsplash.com/photo-1532332248682-206cc786359f?auto=format&fit=crop&q=80&w=600",
            [
                "White",
                "Desert Tan",
                "Navy"
            ]
        ],
        [
            "Rogue Fitness",
            "SR-1 Bearing Speed Rope",
            26.5,
            "High-performance jump rope with precision bearings for smooth, double-under turning.",
            "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&q=80&w=600",
            [
                "Black Cable",
                "Red Cable"
            ]
        ],
        [
            "Marmot",
            "Trestles 15 Mummy Sleeping Bag",
            139.0,
            "Reliable all-purpose synthetic bag designed for backpacking and mountaineering.",
            "https://images.unsplash.com/photo-1537249148386-89c02506b3cc?auto=format&fit=crop&q=80&w=600",
            [
                "Cobalt Blue/Blue Night"
            ]
        ],
        [
            "TheraBand",
            "Pro Series SCP Exercise Ball",
            34.99,
            "Slow deflate exercise ball providing maximum stability and durability.",
            "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?auto=format&fit=crop&q=80&w=600",
            [
                "Blue (65cm)",
                "Silver (75cm)",
                "Red (55cm)"
            ]
        ],
        [
            "Giro",
            "Fixture MIPS Adult Cycling Helmet",
            65.0,
            "Mountain biking helmet with integrated MIPS safety system and removable visor.",
            "https://images.unsplash.com/photo-1541625602330-2277a4c46182?auto=format&fit=crop&q=80&w=600",
            [
                "Matte Black",
                "Matte Grey"
            ]
        ],
        [
            "Black Diamond",
            "Trail Trekking Poles",
            119.95,
            "Durable, dual FlickLock aluminum poles providing exceptional support on the trail.",
            "https://images.unsplash.com/photo-1551632811-561732d1e306?auto=format&fit=crop&q=80&w=600",
            [
                "Picante Red",
                "Granite"
            ]
        ],
        [
            "Under Armour",
            "Undeniable 5.0 Duffle Bag",
            50.0,
            "Tough, water-resistant duffel bag packed with functional pockets including a vented shoe pocket.",
            "https://images.unsplash.com/photo-1547949003-9792a18a2601?auto=format&fit=crop&q=80&w=600",
            [
                "Black",
                "Pitch Grey",
                "Midnight Navy"
            ]
        ]
    ]
}

def get_price_range(price):
    try:
        p = float(price)
        if p < 50: return 'budget'
        if p < 150: return 'mid-range'
        if p < 500: return 'premium'
        return 'luxury'
    except:
        return 'unknown'

def build_tags(category, brand, name):
    cat = category.lower()
    brand = brand.lower()
    name = name.lower()
    tags = [cat, brand]
    if 'wireless' in name or 'bluetooth' in name: tags.append('wireless')
    if 'smart' in name: tags.append('smart')
    if 'leather' in name: tags.append('leather')
    if 'water' in name or 'waterproof' in name: tags.append('waterproof')
    if '4k' in name: tags.append('4k')
    return ','.join(set(tags))

def build_features(category):
    if category == 'Electronics': return 'High performance,1 year warranty,Premium quality'
    if category == 'Shoes': return 'Comfortable fit,Durable outsole,Breathable material'
    if category == 'Clothing': return 'Machine washable,Premium fabric,Regular fit'
    if category == 'Accessories': return 'Durable build,Stylish design,Everyday carry'
    if category == 'Home & Kitchen': return 'Easy to clean,Durable construction,Kitchen essential'
    return 'Premium quality,Durable build'

def validate_dataset(products):
    """Ensure strictly valid data properties."""
    image_to_category = {}
    seen_names = set()
    
    for p in products:
        # Check strict category image mapping
        if p['image_url'] in image_to_category:
            if image_to_category[p['image_url']] != p['category']:
                raise ValueError(f"CRITICAL ERROR: Image {p['image_url']} used in multiple categories!")
        else:
            image_to_category[p['image_url']] = p['category']
            
        # Check unique names
        if p['name'] in seen_names:
            raise ValueError(f"CRITICAL ERROR: Duplicate product name: {p['name']}")
        seen_names.add(p['name'])
        
        # Check missing metadata
        if not p['price_range'] or not p['tags'] or not p['features']:
            raise ValueError(f"CRITICAL ERROR: Missing metadata on {p['name']}")
    print("[SUCCESS] Validation passed: No cross-category images. Names are unique. Metadata is complete.")

def main():
    print("Generating curated realistic dataset...")
    products = []
    pid = 1
    
    for category, items in CATALOG.items():
        for brand, base_name, price, desc, img_url, variants in items:
            for variant in variants:
                # Add slight price variations per color/size
                variant_price = price + round(random.uniform(0, 15), 2) if len(variants) > 1 else price
                rating = round(random.uniform(4.0, 5.0), 1) # Curated products have high ratings
                
                name = f"{brand} {base_name} - {variant}" if variant != "Standard" and variant != "Body Only" else f"{brand} {base_name}"
                
                tags = build_tags(category, brand, name)
                features = build_features(category)
                price_range = get_price_range(variant_price)
                
                encoded_name = urllib.parse.quote_plus(name)
                amz = f"https://www.amazon.in/s?k={encoded_name}"
                fk = f"https://www.flipkart.com/search?q={encoded_name}"
                cat_slug = category.lower().replace(' ', '-')
                myn = f"https://www.myntra.com/{cat_slug}?rawQuery={encoded_name}" if category in ['Clothing', 'Shoes', 'Accessories'] else ""
                
                products.append({
                    'id': pid,
                    'name': name,
                    'category': category,
                    'brand': brand,
                    'price': round(variant_price, 2),
                    'rating': rating,
                    'image_url': img_url,
                    'description': desc,
                    'tags': tags,
                    'features': features,
                    'amazon_url': amz,
                    'flipkart_url': fk,
                    'myntra_url': myn,
                    'price_range': price_range
                })
                pid += 1
                
    # Shuffle slightly but keep IDs sequential
    random.seed(42)
    random.shuffle(products)
    for i, p in enumerate(products):
        p['id'] = i + 1
        
    # Validate
    validate_dataset(products)
    
    # Interactions
    interactions = []
    now = datetime.now()
    six_months_ago = now - timedelta(days=180)
    product_ids = [p['id'] for p in products]
    
    print(f"Generating realistic interactions for {len(products)} products...")
    for _ in range(5000):
        user_id = random.randint(1, 150)
        product_id = random.choice(product_ids)
        timestamp = six_months_ago + timedelta(seconds=random.randint(0, int((now - six_months_ago).total_seconds())))
        
        action_roll = random.random()
        if action_roll < 0.60:
            action = 'click'
            rating_val = None
            purchase = 0
        elif action_roll < 0.85:
            action = 'view'
            rating_val = None
            purchase = 0
        elif action_roll < 0.95:
            action = 'purchase'
            rating_val = round(random.uniform(4.0, 5.0), 1)
            purchase = 1
        else:
            action = 'rating'
            rating_val = round(random.uniform(3.0, 5.0), 1)
            purchase = 0
            
        interactions.append({
            'user_id': user_id,
            'product_id': product_id,
            'action': action,
            'rating': rating_val if rating_val else "",
            'purchase': purchase,
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
        
    # Write CSV
    with open(PRODUCTS_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(products[0].keys()))
        writer.writeheader()
        writer.writerows(products)
        
    with open(INTERACTIONS_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['user_id', 'product_id', 'action', 'rating', 'purchase', 'timestamp'])
        writer.writeheader()
        writer.writerows(interactions)
        
    print(f"Done! Created {len(products)} perfectly curated products and {len(interactions)} interactions.")

if __name__ == "__main__":
    main()
