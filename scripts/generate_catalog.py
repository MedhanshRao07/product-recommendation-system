import json
import random
import urllib.parse
import os

OUTPUT_SQL = os.path.join(os.path.dirname(__file__), '..', 'datasets', 'catalog_seed.sql')

CATEGORIES = {
    "Electronics": {
        "count": 200,
        "subcategories": {
            "Headphones": {
                "brands": ["Sony", "Bose", "Apple", "Sennheiser", "JBL"],
                "images": ["1618366712010-f4ae9c647dcb", "1606220588913-b3aea9ebb173", "1505740420928-5e560c06d30e", "1583394838336-d2b1b9e46ea4", "1484704849700-f032a568e944"],
                "models": ["WH-1000XM5", "QuietComfort 45", "AirPods Max", "Momentum 4", "Live 660NC", "Elite 85h", "HD 600"],
                "tags": ["wireless", "noise-canceling", "bluetooth", "over-ear", "audio"]
            },
            "Keyboards": {
                "brands": ["Logitech", "Corsair", "Razer", "Keychron", "Ducky"],
                "images": ["1605445207797-200a747cf995", "1587829741395-de6a0b830e3c", "1595044426077-d36d9236d54a"],
                "models": ["MX Mechanical", "K70 RGB", "BlackWidow V3", "K8 Pro", "One 3 Mini", "G915 TKL"],
                "tags": ["mechanical", "wireless", "rgb", "typing", "productivity"]
            },
            "Mice": {
                "brands": ["Logitech", "Razer", "SteelSeries", "Corsair"],
                "images": ["1628173549725-3b978fc964b7", "1615663245857-fb8f59e2b5f8"],
                "models": ["MX Master 3S", "DeathAdder V2", "Aerox 3", "Dark Core RGB", "G Pro X Superlight"],
                "tags": ["wireless", "ergonomic", "optical", "productivity"]
            },
            "Monitors": {
                "brands": ["Dell", "LG", "Samsung", "ASUS", "BenQ"],
                "images": ["1527443154391-507e9dc6c5cc", "1585792180666-f7347c490ee2"],
                "models": ["UltraSharp U2723QE", "27GN950-B", "Odyssey G7", "ProArt Display", "PD2700U"],
                "tags": ["4k", "ips", "usb-c", "display", "monitor"]
            },
            "Chargers": {
                "brands": ["Anker", "Belkin", "Apple", "Samsung", "Spigen"],
                "images": ["1609091839311-d5365f9ff1c5", "1610296669228-602d98b41a9e"],
                "models": ["Nano II 65W", "BoostCharge Pro", "20W USB-C", "45W PD", "ArcStation Pro"],
                "tags": ["gan", "fast-charging", "usb-c", "power", "adapter"]
            },
            "Speakers": {
                "brands": ["JBL", "Bose", "Sonos", "Ultimate Ears", "Sony"],
                "images": ["1608043152269-423dbba4e7e1", "1545454675-7dc0e673d35e"],
                "models": ["Charge 5", "SoundLink Revolve+", "Roam", "BOOM 3", "SRS-XB43"],
                "tags": ["bluetooth", "portable", "waterproof", "audio", "speaker"]
            },
            "Laptops": {
                "brands": ["Apple", "Dell", "HP", "Lenovo", "ASUS"],
                "images": ["1593642632823-8f785ba67e45", "1496181133206-80ce9b88a853", "1541807084-5c97b6b991b7"],
                "models": ["MacBook Pro 14", "XPS 15", "Spectre x360", "ThinkPad X1 Carbon", "ZenBook 14"],
                "tags": ["laptop", "ultrabook", "productivity", "portable", "computer"]
            },
            "Smartwatches": {
                "brands": ["Apple", "Samsung", "Garmin", "Fitbit", "Amazfit"],
                "images": ["1546868871-af0de0aafa64", "1579586337278-3befd40fd17a", "1523275335684-37898b6baf30"],
                "models": ["Watch Series 9", "Galaxy Watch 6", "Fenix 7", "Sense 2", "GTR 4"],
                "tags": ["smartwatch", "fitness", "wearable", "health", "tracker"]
            },
            "Tablets": {
                "brands": ["Apple", "Samsung", "Lenovo", "Microsoft", "Amazon"],
                "images": ["1544244015-0df4b3ffc6b0", "1585790050230-5dd28404ccf6"],
                "models": ["iPad Pro 11", "Galaxy Tab S9", "Tab P11 Pro", "Surface Pro 9", "Fire HD 10"],
                "tags": ["tablet", "touchscreen", "portable", "entertainment", "device"]
            },
            "Cameras": {
                "brands": ["Sony", "Canon", "Nikon", "Fujifilm", "Panasonic"],
                "images": ["1516035069371-29a1b244cc32", "1502920917128-1aa500764cbd"],
                "models": ["A7 IV", "EOS R6", "Z6 II", "X-T5", "Lumix GH6"],
                "tags": ["camera", "mirrorless", "photography", "video", "4k"]
            },
            "Mobile Accessories": {
                "brands": ["Spigen", "OtterBox", "PopSockets", "Anker", "Belkin"],
                "images": ["1601784551446-20c9e07cdbdb", "1603791440277-ef23dd0f4293"],
                "models": ["Tough Armor Case", "Symmetry Series", "PopGrip", "PowerLine III Cable", "MagSafe Stand"],
                "tags": ["case", "cable", "stand", "mobile", "accessory"]
            }
        }
    },
    "Fashion": {
        "count": 120,
        "subcategories": {
            "Hoodies": {
                "brands": ["Nike", "Adidas", "Champion", "H&M", "Zara"],
                "images": ["1556821840-3a63f95609a7", "1620799140188-3b2a02fd9a77"],
                "models": ["Sportswear Club Fleece", "Essentials Hoodie", "Reverse Weave Pullover", "Relaxed Fit Hoodie", "Basic Hoodie"],
                "tags": ["hoodie", "sweatshirt", "casual", "winter", "clothing"]
            },
            "T-shirts": {
                "brands": ["Uniqlo", "Levi's", "Nike", "Adidas", "Ralph Lauren"],
                "images": ["1581655353564-df123a1eb820", "1521572163474-6864f9cf17ab"],
                "models": ["Supima Cotton Crew Neck", "Graphic Tee", "Dri-FIT Tee", "Trefoil T-Shirt", "Classic Fit Polo"],
                "tags": ["t-shirt", "tee", "casual", "summer", "clothing"]
            },
            "Jackets": {
                "brands": ["The North Face", "Patagonia", "Levi's", "Zara", "Columbia"],
                "images": ["1551028719-00167b16eac5", "1591047139829-d9d13e3bc891"],
                "models": ["Nuptse Jacket", "Better Sweater", "Trucker Jacket", "Puffer Jacket", "Fleece Jacket"],
                "tags": ["jacket", "outerwear", "winter", "warm", "clothing"]
            },
            "Jeans": {
                "brands": ["Levi's", "Wrangler", "Lee", "Calvin Klein", "Diesel"],
                "images": ["1542272604-787c3835535d", "1541099649105-f69ad21f3246"],
                "models": ["501 Original Fit", "Texas Stretch", "Luke Slim Tapered", "Slim Straight", "Sleenker Skinny"],
                "tags": ["jeans", "denim", "pants", "casual", "clothing"]
            },
            "Shirts": {
                "brands": ["Ralph Lauren", "Tommy Hilfiger", "Brooks Brothers", "Hugo Boss", "Zara"],
                "images": ["1596755094514-f87e34085b2c", "1598032895397-b0b68917a24a"],
                "models": ["Oxford Cloth Button-Down", "Custom Fit Shirt", "Non-Iron Dress Shirt", "Slim Fit Poplin", "Linen Shirt"],
                "tags": ["shirt", "button-down", "formal", "casual", "clothing"]
            },
            "Dresses": {
                "brands": ["H&M", "Zara", "ASOS", "Mango", "Reformation"],
                "images": ["1560971037-7fba0bfe688b", "1595777457583-95e4f5d7b5f8"],
                "models": ["Slip Dress", "Midi Dress", "Wrap Dress", "Maxi Dress", "Floral Dress"],
                "tags": ["dress", "womenswear", "elegant", "summer", "clothing"]
            },
            "Sweaters": {
                "brands": ["Uniqlo", "J.Crew", "Banana Republic", "Everlane", "Massimo Dutti"],
                "images": ["1617326857907-7e04918e6922", "1543076447-215ad9ba6923"],
                "models": ["Cashmere Crewneck", "Merino Wool V-Neck", "Cotton Cable Knit", "Alpaca Sweater", "Turtleneck Sweater"],
                "tags": ["sweater", "knitwear", "winter", "warm", "clothing"]
            }
        }
    },
    "Shoes": {
        "count": 80,
        "subcategories": {
            "Sneakers": {
                "brands": ["Nike", "Adidas", "Puma", "New Balance", "Vans"],
                "images": ["1595950653106-6c9ebd614d3a", "1491553895911-0055eca6402d", "1539185441755-769473a23570"],
                "models": ["Air Force 1", "Superstar", "Suede Classic", "574 Core", "Old Skool"],
                "tags": ["sneakers", "casual", "footwear", "streetwear", "shoes"]
            },
            "Running": {
                "brands": ["Nike", "Adidas", "ASICS", "Brooks", "Hoka"],
                "images": ["1608231387042-66d1773070a5", "1600185365483-26d7a4cc7519"],
                "models": ["Air Zoom Pegasus", "Ultraboost 22", "Gel-Kayano 29", "Ghost 15", "Clifton 9"],
                "tags": ["running", "sports", "athletic", "performance", "shoes"]
            },
            "Boots": {
                "brands": ["Dr. Martens", "Timberland", "Blundstone", "Red Wing", "Clarks"],
                "images": ["1520639888713-7851133b1ed0", "1511556820780-d912e42b4980"],
                "models": ["1460 Smooth Leather Boot", "6-Inch Premium Boot", "Classic 550 Chelsea", "Iron Ranger", "Desert Boot"],
                "tags": ["boots", "leather", "durable", "winter", "shoes"]
            },
            "Casual": {
                "brands": ["Converse", "Skechers", "TOMS", "Crocs", "Sperry"],
                "images": ["1525966222134-fcfa99b8ae77", "1588361861040-ac9b1018f6d5"],
                "models": ["Chuck Taylor All Star", "Go Walk", "Classic Alpargata", "Classic Clog", "Authentic Original Boat Shoe"],
                "tags": ["casual", "comfortable", "everyday", "slip-on", "shoes"]
            },
            "Formal": {
                "brands": ["Cole Haan", "Allen Edmonds", "Johnston & Murphy", "Hugo Boss", "Clarks"],
                "images": ["1614252235316-8c857d38b5f4", "1449505278894-297fdb3ed98"],
                "models": ["Oxford Dress Shoe", "Park Avenue Cap-Toe", "Melton Oxford", "Derby Shoe", "Tilden Cap Oxford"],
                "tags": ["formal", "leather", "dress", "office", "shoes"]
            }
        }
    },
    "Bags": {
        "count": 80,
        "subcategories": {
            "Backpacks": {
                "brands": ["Herschel", "JanSport", "The North Face", "Fjallraven", "Samsonite"],
                "images": ["1553062407-98eeb64c6a62", "1581605405669-fcdf81fc23c3"],
                "models": ["Little America", "Right Pack", "Borealis", "Kanken", "Xenon 3.0"],
                "tags": ["backpack", "travel", "school", "carry", "bag"]
            },
            "Handbags": {
                "brands": ["Michael Kors", "Kate Spade", "Coach", "Fossil", "Gucci"],
                "images": ["1548036328-c896dce5a7f8", "1584917865442-de89d68e5c43"],
                "models": ["Jet Set Tote", "Margaux Satchel", "Tabby Shoulder Bag", "Rachel Tote", "Marmont Matelasse"],
                "tags": ["handbag", "purse", "designer", "leather", "accessory"]
            },
            "Laptop Bags": {
                "brands": ["Targus", "Case Logic", "Incase", "Tomtoc", "Samsonite"],
                "images": ["1622560480654-d96214fdc887", "1547949003-9d1a72dad6c2"],
                "models": ["CityLite Briefcase", "Laptop Sleeve", "City Backpack", "Defender Sleeve", "Colombian Leather Flapover"],
                "tags": ["laptop-bag", "work", "briefcase", "office", "bag"]
            },
            "Duffel Bags": {
                "brands": ["Nike", "Adidas", "Under Armour", "Patagonia", "Herschel"],
                "images": ["1553062407-98eeb64c6a62", "1445941340-7c69e4f4eb60"],
                "models": ["Brasilia Duffel", "Defender Duffel", "Undeniable 5.0", "Black Hole Duffel", "Novel Duffel"],
                "tags": ["duffel", "gym", "travel", "weekend", "bag"]
            }
        }
    },
    "Accessories": {
        "count": 100,
        "subcategories": {
            "Watches": {
                "brands": ["Casio", "Seiko", "Fossil", "Tissot", "Citizen"],
                "images": ["1524805444758-089113d48a6d", "1549972352-7104fded7a30", "1622329618074-d4b9981ed73e"],
                "models": ["G-Shock Classic", "5 Sports Automatic", "Grant Chronograph", "PRX Powermatic 80", "Eco-Drive Promaster"],
                "tags": ["watch", "timepiece", "analog", "wrist", "accessory"]
            },
            "Sunglasses": {
                "brands": ["Ray-Ban", "Oakley", "Persol", "Prada", "Maui Jim"],
                "images": ["1511499767150-a48a237f0083", "1559564177-d0c3c8f8d689"],
                "models": ["Classic Wayfarer", "Holbrook", "714 Folding", "Linea Rossa", "Peahi Polarized"],
                "tags": ["sunglasses", "eyewear", "summer", "uv-protection", "accessory"]
            },
            "Wallets": {
                "brands": ["Bellroy", "Fossil", "Tommy Hilfiger", "Secrid", "Timberland"],
                "images": ["1627123424574-724758594e93", "1548036328-c896dce5a7f8"],
                "models": ["Note Sleeve", "Derrick Bifold", "Leather Passcase", "Slim Wallet", "Hunter Trifold"],
                "tags": ["wallet", "leather", "slim", "rfid", "accessory"]
            },
            "Belts": {
                "brands": ["Levi's", "Calvin Klein", "Gucci", "Tommy Hilfiger", "Dickies"],
                "images": ["1603808033192-082d6919d3e1", "1594938328870-c67e3d728f1f"],
                "models": ["Reversible Leather Belt", "Classic Logo Belt", "GG Marmont Belt", "Stretch Belt", "Web Belt"],
                "tags": ["belt", "leather", "casual", "formal", "accessory"]
            }
        }
    },
    "Fitness": {
        "count": 100,
        "subcategories": {
            "Dumbbells": {
                "brands": ["Bowflex", "CAP Barbell", "Rogue", "Amazon Basics", "Yes4All"],
                "images": ["1534438327276-14e5300c3a48", "1571019613454-1cb2f99b2d8b", "1576678927484-cc907957088c", "1598971639058-feb753d2ee06"],
                "models": ["SelectTech 552", "Hex Dumbbell Set", "Rubber Hex Dumbbells", "Neoprene Dumbbell", "Adjustable Dumbbells"],
                "tags": ["dumbbells", "weights", "strength", "home-gym", "fitness"]
            },
            "Yoga Mats": {
                "brands": ["Manduka", "Lululemon", "Gaiam", "JadeYoga", "Alo Yoga"],
                "images": ["1534438327276-14e5300c3a48", "1571019613454-1cb2f99b2d8b", "1576678927484-cc907957088c", "1598971639058-feb753d2ee06"],
                "models": ["PRO Yoga Mat", "The Reversible Mat", "Premium Print Mat", "Harmony Mat", "Warrior Mat"],
                "tags": ["yoga", "mat", "stretching", "pilates", "fitness"]
            },
            "Resistance Bands": {
                "brands": ["TheraBand", "Gritin", "Fit Simplify", "Undersun", "SPRI"],
                "images": ["1534438327276-14e5300c3a48", "1571019613454-1cb2f99b2d8b", "1576678927484-cc907957088c", "1598971639058-feb753d2ee06"],
                "models": ["Professional Latex Bands", "Resistance Loop Exercise Bands", "Set of 5 Bands", "Fitness Bands", "Xertube Resistance Band"],
                "tags": ["resistance", "bands", "workout", "home-gym", "fitness"]
            },
            "Foam Rollers": {
                "brands": ["TriggerPoint", "Amazon Basics", "LuxFit", "OPTP", "Brazyn"],
                "images": ["1534438327276-14e5300c3a48", "1571019613454-1cb2f99b2d8b", "1576678927484-cc907957088c", "1598971639058-feb753d2ee06"],
                "models": ["GRID Foam Roller", "High-Density Foam Roller", "Speckled Foam Roller", "Pro-Roller Standard", "Morph Collapsible Roller"],
                "tags": ["recovery", "massage", "foam-roller", "stretching", "fitness"]
            },
            "Protein Shakers": {
                "brands": ["BlenderBottle", "ShakeSphere", "Hydra Cup", "Helimix", "Promixx"],
                "images": ["1534438327276-14e5300c3a48", "1571019613454-1cb2f99b2d8b", "1576678927484-cc907957088c", "1598971639058-feb753d2ee06"],
                "models": ["Classic V2", "Tumbler", "Dual Shaker", "Vortex Shaker", "Pro Shaker"],
                "tags": ["shaker", "protein", "bottle", "gym", "fitness"]
            },
             "Fitness Trackers": {
                "brands": ["Fitbit", "Garmin", "Xiaomi", "Amazfit", "WHOOP"],
                 "images": ["1534438327276-14e5300c3a48", "1571019613454-1cb2f99b2d8b", "1576678927484-cc907957088c", "1598971639058-feb753d2ee06"],
                "models": ["Charge 5", "Vivosmart 5", "Mi Band 7", "Band 7", "WHOOP 4.0"],
                "tags": ["tracker", "wearable", "health", "steps", "fitness"]
            }
        }
    },
    "Sports": {
        "count": 100,
        "subcategories": {
            "Cricket": {
                "brands": ["SG", "SS", "Kookaburra", "Gray-Nicolls", "MRF"],
                "images": ["1531415074968-036ba1b575da", "1579952363873-f5c7deff2e99", "1461896836934-ffe607ba8211"],
                "models": ["Players Bat", "Ton Gladiator", "Kahuna Pro", "Vapor 1.0", "Genius Grand Edition"],
                "tags": ["cricket", "bat", "sports", "outdoor", "team"]
            },
            "Football": {
                "brands": ["Nike", "Adidas", "Puma", "Mitre", "Select"],
                "images": ["1531415074968-036ba1b575da", "1579952363873-f5c7deff2e99", "1461896836934-ffe607ba8211"],
                "models": ["Flight Ball", "Al Rihla Pro", "La Liga 1", "Delta Professional", "Brillant Super"],
                "tags": ["football", "soccer", "ball", "sports", "outdoor"]
            },
            "Basketball": {
                "brands": ["Spalding", "Wilson", "Nike", "Under Armour", "Molten"],
                "images": ["1531415074968-036ba1b575da", "1579952363873-f5c7deff2e99", "1461896836934-ffe607ba8211"],
                "models": ["NBA Official Game Ball", "Evolution Game Basketball", "Elite Championship", "495 Indoor", "BG5000"],
                "tags": ["basketball", "hoops", "sports", "indoor", "ball"]
            },
            "Tennis": {
                "brands": ["Wilson", "Babolat", "HEAD", "Yonex", "Prince"],
                "images": ["1531415074968-036ba1b575da", "1579952363873-f5c7deff2e99", "1461896836934-ffe607ba8211"],
                "models": ["Pro Staff 97", "Pure Drive", "Radical MP", "EZONE 98", "Phantom 100"],
                "tags": ["tennis", "racket", "sports", "outdoor", "court"]
            },
            "Badminton": {
                "brands": ["Yonex", "Victor", "Li-Ning", "Apacs", "Carlton"],
                "images": ["1531415074968-036ba1b575da", "1579952363873-f5c7deff2e99", "1461896836934-ffe607ba8211"],
                "models": ["Astrox 99 Pro", "Thruster F", "Aeronaut 9000", "Z-Ziggler", "Kinesis 80S"],
                "tags": ["badminton", "racket", "shuttlecock", "sports", "indoor"]
            }
        }
    },
    "Gaming": {
        "count": 100,
        "subcategories": {
            "Controllers": {
                "brands": ["Sony", "Microsoft", "Nintendo", "Razer", "8BitDo"],
                "images": ["1612287230202-1ff1d85d1bdf", "1593305841991-05c297ba4575", "1616588589676-62b3d4ff6e36"],
                "models": ["DualSense Wireless", "Xbox Elite Series 2", "Pro Controller", "Wolverine V2", "Ultimate Bluetooth"],
                "tags": ["controller", "gamepad", "gaming", "console", "pc"]
            },
            "Gaming Keyboards": {
                "brands": ["Razer", "Corsair", "SteelSeries", "Logitech G", "HyperX"],
                "images": ["1612287230202-1ff1d85d1bdf", "1593305841991-05c297ba4575", "1616588589676-62b3d4ff6e36"],
                "models": ["Huntsman V2", "K100 RGB", "Apex Pro TKL", "G915 Lightspeed", "Alloy Origins"],
                "tags": ["keyboard", "mechanical", "rgb", "gaming", "pc"]
            },
            "Gaming Mice": {
                "brands": ["Logitech G", "Razer", "SteelSeries", "Glorious", "Roccat"],
                "images": ["1612287230202-1ff1d85d1bdf", "1593305841991-05c297ba4575", "1616588589676-62b3d4ff6e36"],
                "models": ["G Pro X Superlight", "DeathAdder V3 Pro", "Aerox 5 Wireless", "Model O", "Kone Pro Air"],
                "tags": ["mouse", "gaming", "rgb", "wireless", "pc"]
            },
            "Headsets": {
                "brands": ["HyperX", "SteelSeries", "Razer", "Logitech G", "Astro"],
                "images": ["1612287230202-1ff1d85d1bdf", "1593305841991-05c297ba4575", "1616588589676-62b3d4ff6e36"],
                "models": ["Cloud II Wireless", "Arctis Nova Pro", "BlackShark V2 Pro", "PRO X Wireless", "A50 Wireless"],
                "tags": ["headset", "audio", "mic", "gaming", "surround"]
            },
            "Gaming Chairs": {
                "brands": ["Secretlab", "Noblechairs", "Corsair", "Razer", "DXRacer"],
                "images": ["1612287230202-1ff1d85d1bdf", "1593305841991-05c297ba4575", "1616588589676-62b3d4ff6e36"],
                "models": ["Titan Evo 2022", "Hero Series", "T3 Rush", "Iskur", "Formula Series"],
                "tags": ["chair", "ergonomic", "gaming", "comfort", "setup"]
            }
        }
    },
    "Home Appliances": {
        "count": 120,
        "subcategories": {
            "Kitchen": {
                "brands": ["Instant Pot", "Ninja", "Breville", "KitchenAid", "Philips"],
                "images": ["1585659722983-3a675dabf23d", "1556909114-f6e7ad7d3136", "1544568100-4c60e3220241"],
                "models": ["Duo 7-in-1", "Foodi Air Fryer", "Barista Express", "Artisan Stand Mixer", "Essential Airfryer"],
                "tags": ["kitchen", "cooking", "appliance", "home", "food"]
            },
            "Cleaning": {
                "brands": ["Dyson", "Shark", "iRobot", "Bissell", "Miele"],
                "images": ["1585659722983-3a675dabf23d", "1556909114-f6e7ad7d3136", "1544568100-4c60e3220241"],
                "models": ["V15 Detect", "Navigator Lift-Away", "Roomba j7+", "CrossWave", "Complete C3"],
                "tags": ["cleaning", "vacuum", "home", "appliance", "smart"]
            },
            "Coffee Makers": {
                "brands": ["Keurig", "Nespresso", "Breville", "De'Longhi", "Hamilton Beach"],
                "images": ["1585659722983-3a675dabf23d", "1556909114-f6e7ad7d3136", "1544568100-4c60e3220241"],
                "models": ["K-Elite", "VertuoPlus", "Bambino Plus", "Magnifica S", "FlexBrew"],
                "tags": ["coffee", "espresso", "morning", "kitchen", "appliance"]
            },
            "Air Purifiers": {
                "brands": ["Coway", "Levoit", "Dyson", "Winix", "Blueair"],
                "images": ["1585659722983-3a675dabf23d", "1556909114-f6e7ad7d3136", "1544568100-4c60e3220241"],
                "models": ["Airmega 400", "Core 400S", "Purifier Cool", "5500-2", "Blue Pure 211+"],
                "tags": ["air-purifier", "clean-air", "home", "appliance", "health"]
            }
        }
    }
}

def escape_sql(text):
    return str(text).replace("'", "''")

def get_price_range(price):
    if price < 50:
        return "budget"
    elif price < 200:
        return "mid-range"
    elif price < 800:
        return "premium"
    else:
        return "luxury"

def generate_products():
    products = []
    
    for category_name, cat_data in CATEGORIES.items():
        target_count = cat_data["count"]
        subcategories = list(cat_data["subcategories"].keys())
        
        # distribute count roughly evenly among subcategories
        count_per_sub = target_count // len(subcategories)
        rem = target_count % len(subcategories)
        
        for i, subcat_name in enumerate(subcategories):
            subcat_data = cat_data["subcategories"][subcat_name]
            num_to_generate = count_per_sub + (1 if i < rem else 0)
            
            for _ in range(num_to_generate):
                brand = random.choice(subcat_data["brands"])
                model = random.choice(subcat_data["models"])
                
                # add some variation to model name to make it unique-ish
                variation = ""
                if random.random() < 0.3:
                    variation = f" {random.choice(['Pro', 'Max', 'Plus', 'Ultra', 'Elite', 'V2', 'Edition'])}"
                
                name = f"{brand} {model}{variation}"
                
                # generate price based on category
                base_price = 100
                if category_name in ["Electronics", "Home Appliances"]:
                    base_price = random.uniform(50, 1500)
                elif category_name in ["Gaming"]:
                    base_price = random.uniform(30, 800)
                elif category_name in ["Fashion", "Shoes", "Bags"]:
                    base_price = random.uniform(20, 300)
                elif category_name in ["Accessories", "Fitness", "Sports"]:
                    base_price = random.uniform(10, 200)
                    
                price = round(base_price, 2)
                price_range = get_price_range(price)
                
                rating = round(random.uniform(3.5, 5.0), 1)
                popularity_score = round(random.uniform(0.1, 0.99), 2)
                
                image_id = random.choice(subcat_data["images"])
                image_url = f"https://images.unsplash.com/photo-{image_id}?auto=format&fit=crop&q=80&w=600"
                
                tags = subcat_data["tags"].copy()
                if brand.lower() not in [t.lower() for t in tags]:
                    tags.append(brand.lower())
                random.shuffle(tags)
                tags_str = ",".join(tags)
                
                description = f"Premium {subcat_name.lower()} by {brand}. The {name} features top-tier quality and performance. Perfect for {category_name.lower()} enthusiasts."
                features = f"High quality|Durable design|Premium materials|Authentic {brand} product"
                
                encoded_name = urllib.parse.quote(name)
                amazon_url = f"https://www.amazon.in/s?k={encoded_name}"
                flipkart_url = f"https://www.flipkart.com/search?q={encoded_name}"
                
                myntra_url = ""
                if category_name in ["Fashion", "Shoes", "Bags", "Accessories"]:
                    myntra_url = f"https://www.myntra.com/{encoded_name}"
                
                products.append({
                    "name": name,
                    "category": category_name,
                    "subcategory": subcat_name,
                    "brand": brand,
                    "price": price,
                    "rating": rating,
                    "image_url": image_url,
                    "description": description,
                    "tags": tags_str,
                    "features": features,
                    "amazon_url": amazon_url,
                    "flipkart_url": flipkart_url,
                    "myntra_url": myntra_url,
                    "price_range": price_range,
                    "popularity_score": popularity_score
                })
                
    return products

def main():
    print("Generating products...")
    products = generate_products()
    print(f"Total products generated: {len(products)}")
    
    # write to SQL
    print(f"Writing SQL to {OUTPUT_SQL}...")
    with open(OUTPUT_SQL, 'w', encoding='utf-8') as f:
        f.write("SET FOREIGN_KEY_CHECKS = 0;\n")
        f.write("TRUNCATE TABLE products;\n")
        f.write("SET FOREIGN_KEY_CHECKS = 1;\n\n")
        
        # Batch insert
        batch_size = 100
        for i in range(0, len(products), batch_size):
            batch = products[i:i+batch_size]
            
            sql = "INSERT INTO products (name, category, subcategory, brand, price, rating, image_url, description, tags, features, amazon_url, flipkart_url, myntra_url, price_range, popularity_score) VALUES\n"
            
            values = []
            for p in batch:
                val = f"('{escape_sql(p['name'])}', '{escape_sql(p['category'])}', '{escape_sql(p['subcategory'])}', '{escape_sql(p['brand'])}', {p['price']}, {p['rating']}, '{escape_sql(p['image_url'])}', '{escape_sql(p['description'])}', '{escape_sql(p['tags'])}', '{escape_sql(p['features'])}', '{escape_sql(p['amazon_url'])}', '{escape_sql(p['flipkart_url'])}', '{escape_sql(p['myntra_url'])}', '{escape_sql(p['price_range'])}', {p['popularity_score']})"
                values.append(val)
                
            sql += ",\n".join(values) + ";\n\n"
            f.write(sql)
            
    print("SQL generation complete.")

if __name__ == "__main__":
    main()
