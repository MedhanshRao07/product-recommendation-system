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
                "brand_models": {
                    "Sony": ["WH-1000XM5"],
                    "Bose": ["QuietComfort 45"],
                    "Apple": ["AirPods Max"],
                    "Sennheiser": ["Momentum 4", "HD 600"],
                    "JBL": ["Live 660NC"],
                    "Jabra": ["Elite 85h"]
                },
                "images": ["1618366712010-f4ae9c647dcb", "1606220588913-b3aea9ebb173", "1505740420928-5e560c06d30e", "1583394838336-d2b1b9e46ea4", "1484704849700-f032a568e944"],
                "tags": ["wireless", "noise-canceling", "bluetooth", "over-ear", "audio"]
            },
            "Keyboards": {
                "brand_models": {
                    "Logitech": ["MX Mechanical", "G915 TKL"],
                    "Corsair": ["K70 RGB"],
                    "Razer": ["BlackWidow V3"],
                    "Keychron": ["K8 Pro"],
                    "Ducky": ["One 3 Mini"]
                },
                "images": ["1605445207797-200a747cf995", "1587829741395-de6a0b830e3c", "1595044426077-d36d9236d54a"],
                "tags": ["mechanical", "wireless", "rgb", "typing", "productivity"]
            },
            "Mice": {
                "brand_models": {
                    "Logitech": ["MX Master 3S", "G Pro X Superlight"],
                    "Razer": ["DeathAdder V2"],
                    "SteelSeries": ["Aerox 3"],
                    "Corsair": ["Dark Core RGB"]
                },
                "images": ["1628173549725-3b978fc964b7", "1615663245857-fb8f59e2b5f8"],
                "tags": ["wireless", "ergonomic", "optical", "productivity"]
            },
            "Monitors": {
                "brand_models": {
                    "Dell": ["UltraSharp U2723QE"],
                    "LG": ["27GN950-B"],
                    "Samsung": ["Odyssey G7"],
                    "ASUS": ["ProArt Display"],
                    "BenQ": ["PD2700U"]
                },
                "images": ["1527443154391-507e9dc6c5cc", "1585792180666-f7347c490ee2"],
                "tags": ["4k", "ips", "usb-c", "display", "monitor"]
            },
            "Chargers": {
                "brand_models": {
                    "Anker": ["Nano II 65W"],
                    "Belkin": ["BoostCharge Pro"],
                    "Apple": ["20W USB-C"],
                    "Samsung": ["45W PD"],
                    "Spigen": ["ArcStation Pro"]
                },
                "images": ["1609091839311-d5365f9ff1c5", "1610296669228-602d98b41a9e"],
                "tags": ["gan", "fast-charging", "usb-c", "power", "adapter"]
            },
            "Speakers": {
                "brand_models": {
                    "JBL": ["Charge 5"],
                    "Bose": ["SoundLink Revolve+"],
                    "Sonos": ["Roam"],
                    "Ultimate Ears": ["BOOM 3"],
                    "Sony": ["SRS-XB43"]
                },
                "images": ["1608043152269-423dbba4e7e1", "1545454675-7dc0e673d35e"],
                "tags": ["bluetooth", "portable", "waterproof", "audio", "speaker"]
            },
            "Laptops": {
                "brand_models": {
                    "Apple": ["MacBook Pro 14", "MacBook Air M2"],
                    "Dell": ["XPS 15"],
                    "HP": ["Spectre x360"],
                    "Lenovo": ["ThinkPad X1 Carbon"],
                    "ASUS": ["ZenBook 14"]
                },
                "images": ["1593642632823-8f785ba67e45", "1496181133206-80ce9b88a853", "1541807084-5c97b6b991b7"],
                "tags": ["laptop", "ultrabook", "productivity", "portable", "computer"]
            },
            "Smartwatches": {
                "brand_models": {
                    "Apple": ["Watch Series 9"],
                    "Samsung": ["Galaxy Watch 6"],
                    "Garmin": ["Fenix 7", "Forerunner"],
                    "Fitbit": ["Sense 2"],
                    "Amazfit": ["GTR 4"]
                },
                "images": ["1546868871-af0de0aafa64", "1579586337278-3befd40fd17a", "1523275335684-37898b6baf30"],
                "tags": ["smartwatch", "fitness", "wearable", "health", "tracker"]
            },
            "Tablets": {
                "brand_models": {
                    "Apple": ["iPad Pro 11"],
                    "Samsung": ["Galaxy Tab S9"],
                    "Lenovo": ["Tab P11 Pro"],
                    "Microsoft": ["Surface Pro 9"],
                    "Amazon": ["Fire HD 10"]
                },
                "images": ["1544244015-0df4b3ffc6b0", "1585790050230-5dd28404ccf6"],
                "tags": ["tablet", "touchscreen", "portable", "entertainment", "device"]
            },
            "Cameras": {
                "brand_models": {
                    "Sony": ["A7 IV"],
                    "Canon": ["EOS R6"],
                    "Nikon": ["Z6 II"],
                    "Fujifilm": ["X-T5"],
                    "Panasonic": ["Lumix GH6"]
                },
                "images": ["1516035069371-29a1b244cc32", "1502920917128-1aa500764cbd"],
                "tags": ["camera", "mirrorless", "photography", "video", "4k"]
            },
            "Mobile Accessories": {
                "brand_models": {
                    "Spigen": ["Tough Armor Case"],
                    "OtterBox": ["Symmetry Series"],
                    "PopSockets": ["PopGrip"],
                    "Anker": ["PowerLine III Cable"],
                    "Belkin": ["MagSafe Stand"]
                },
                "images": ["1601784551446-20c9e07cdbdb", "1603791440277-ef23dd0f4293"],
                "tags": ["case", "cable", "stand", "mobile", "accessory"]
            }
        }
    },
    "Fashion": {
        "count": 120,
        "subcategories": {
            "Hoodies": {
                "brand_models": {
                    "Nike": ["Sportswear Club Fleece"],
                    "Adidas": ["Essentials Hoodie"],
                    "Champion": ["Reverse Weave Pullover"],
                    "H&M": ["Relaxed Fit Hoodie"],
                    "Zara": ["Basic Hoodie"]
                },
                "images": ["1556821840-3a63f95609a7", "1620799140188-3b2a02fd9a77"],
                "tags": ["hoodie", "sweatshirt", "casual", "winter", "clothing"]
            },
            "T-shirts": {
                "brand_models": {
                    "Uniqlo": ["Supima Cotton Crew Neck"],
                    "Levi's": ["Graphic Tee"],
                    "Nike": ["Dri-FIT Tee"],
                    "Adidas": ["Trefoil T-Shirt"],
                    "Ralph Lauren": ["Classic Fit Polo"]
                },
                "images": ["1581655353564-df123a1eb820", "1521572163474-6864f9cf17ab"],
                "tags": ["t-shirt", "tee", "casual", "summer", "clothing"]
            },
            "Jackets": {
                "brand_models": {
                    "The North Face": ["Nuptse Jacket"],
                    "Patagonia": ["Better Sweater"],
                    "Levi's": ["Trucker Jacket"],
                    "Zara": ["Puffer Jacket"],
                    "Columbia": ["Fleece Jacket"]
                },
                "images": ["1551028719-00167b16eac5", "1591047139829-d9d13e3bc891"],
                "tags": ["jacket", "outerwear", "winter", "warm", "clothing"]
            },
            "Jeans": {
                "brand_models": {
                    "Levi's": ["501 Original Fit"],
                    "Wrangler": ["Texas Stretch"],
                    "Lee": ["Luke Slim Tapered"],
                    "Calvin Klein": ["Slim Straight"],
                    "Diesel": ["Sleenker Skinny"]
                },
                "images": ["1542272604-787c3835535d", "1541099649105-f69ad21f3246"],
                "tags": ["jeans", "denim", "pants", "casual", "clothing"]
            },
            "Shirts": {
                "brand_models": {
                    "Ralph Lauren": ["Oxford Cloth Button-Down"],
                    "Tommy Hilfiger": ["Custom Fit Shirt"],
                    "Brooks Brothers": ["Non-Iron Dress Shirt"],
                    "Hugo Boss": ["Slim Fit Poplin"],
                    "Zara": ["Linen Shirt"]
                },
                "images": ["1596755094514-f87e34085b2c", "1598032895397-b0b68917a24a"],
                "tags": ["shirt", "button-down", "formal", "casual", "clothing"]
            },
            "Dresses": {
                "brand_models": {
                    "H&M": ["Slip Dress"],
                    "Zara": ["Midi Dress"],
                    "ASOS": ["Wrap Dress"],
                    "Mango": ["Maxi Dress"],
                    "Reformation": ["Floral Dress"]
                },
                "images": ["1560971037-7fba0bfe688b", "1595777457583-95e4f5d7b5f8"],
                "tags": ["dress", "womenswear", "elegant", "summer", "clothing"]
            },
            "Sweaters": {
                "brand_models": {
                    "Uniqlo": ["Cashmere Crewneck"],
                    "J.Crew": ["Merino Wool V-Neck"],
                    "Banana Republic": ["Cotton Cable Knit"],
                    "Everlane": ["Alpaca Sweater"],
                    "Massimo Dutti": ["Turtleneck Sweater"]
                },
                "images": ["1617326857907-7e04918e6922", "1543076447-215ad9ba6923"],
                "tags": ["sweater", "knitwear", "winter", "warm", "clothing"]
            }
        }
    },
    "Shoes": {
        "count": 80,
        "subcategories": {
            "Sneakers": {
                "brand_models": {
                    "Nike": ["Air Force 1"],
                    "Adidas": ["Superstar"],
                    "Puma": ["Suede Classic"],
                    "New Balance": ["574 Core"],
                    "Vans": ["Old Skool"]
                },
                "images": ["1595950653106-6c9ebd614d3a", "1491553895911-0055eca6402d", "1539185441755-769473a23570"],
                "tags": ["sneakers", "casual", "footwear", "streetwear", "shoes"]
            },
            "Running": {
                "brand_models": {
                    "Nike": ["Air Zoom Pegasus"],
                    "Adidas": ["Ultraboost 22"],
                    "ASICS": ["Gel-Kayano 29"],
                    "Brooks": ["Ghost 15"],
                    "Hoka": ["Clifton 9"]
                },
                "images": ["1608231387042-66d1773070a5", "1600185365483-26d7a4cc7519"],
                "tags": ["running", "sports", "athletic", "performance", "shoes"]
            },
            "Boots": {
                "brand_models": {
                    "Dr. Martens": ["1460 Smooth Leather Boot"],
                    "Timberland": ["6-Inch Premium Boot"],
                    "Blundstone": ["Classic 550 Chelsea"],
                    "Red Wing": ["Iron Ranger"],
                    "Clarks": ["Desert Boot"]
                },
                "images": ["1520639888713-7851133b1ed0", "1511556820780-d912e42b4980"],
                "tags": ["boots", "leather", "durable", "winter", "shoes"]
            },
            "Casual": {
                "brand_models": {
                    "Converse": ["Chuck Taylor All Star"],
                    "Skechers": ["Go Walk"],
                    "TOMS": ["Classic Alpargata"],
                    "Crocs": ["Classic Clog"],
                    "Sperry": ["Authentic Original Boat Shoe"]
                },
                "images": ["1525966222134-fcfa99b8ae77", "1588361861040-ac9b1018f6d5"],
                "tags": ["casual", "comfortable", "everyday", "slip-on", "shoes"]
            },
            "Formal": {
                "brand_models": {
                    "Cole Haan": ["Oxford Dress Shoe"],
                    "Allen Edmonds": ["Park Avenue Cap-Toe"],
                    "Johnston & Murphy": ["Melton Oxford"],
                    "Hugo Boss": ["Derby Shoe"],
                    "Clarks": ["Tilden Cap Oxford"]
                },
                "images": ["1614252235316-8c857d38b5f4", "1449505278894-297fdb3ed98"],
                "tags": ["formal", "leather", "dress", "office", "shoes"]
            }
        }
    },
    "Bags": {
        "count": 80,
        "subcategories": {
            "Backpacks": {
                "brand_models": {
                    "Herschel": ["Little America"],
                    "JanSport": ["Right Pack"],
                    "The North Face": ["Borealis"],
                    "Fjallraven": ["Kanken"],
                    "Samsonite": ["Xenon 3.0"]
                },
                "images": ["1553062407-98eeb64c6a62", "1581605405669-fcdf81fc23c3"],
                "tags": ["backpack", "travel", "school", "carry", "bag"]
            },
            "Handbags": {
                "brand_models": {
                    "Michael Kors": ["Jet Set Tote"],
                    "Kate Spade": ["Margaux Satchel"],
                    "Coach": ["Tabby Shoulder Bag"],
                    "Fossil": ["Rachel Tote"],
                    "Gucci": ["Marmont Matelasse"]
                },
                "images": ["1548036328-c896dce5a7f8", "1584917865442-de89d68e5c43"],
                "tags": ["handbag", "purse", "designer", "leather", "accessory"]
            },
            "Laptop Bags": {
                "brand_models": {
                    "Targus": ["CityLite Briefcase"],
                    "Case Logic": ["Laptop Sleeve"],
                    "Incase": ["City Backpack"],
                    "Tomtoc": ["Defender Sleeve"],
                    "Samsonite": ["Colombian Leather Flapover"]
                },
                "images": ["1622560480654-d96214fdc887", "1547949003-9d1a72dad6c2"],
                "tags": ["laptop-bag", "work", "briefcase", "office", "bag"]
            },
            "Duffel Bags": {
                "brand_models": {
                    "Nike": ["Brasilia Duffel"],
                    "Adidas": ["Defender Duffel"],
                    "Under Armour": ["Undeniable 5.0"],
                    "Patagonia": ["Black Hole Duffel"],
                    "Herschel": ["Novel Duffel"]
                },
                "images": ["1553062407-98eeb64c6a62", "1445941340-7c69e4f4eb60"],
                "tags": ["duffel", "gym", "travel", "weekend", "bag"]
            }
        }
    },
    "Accessories": {
        "count": 100,
        "subcategories": {
            "Watches": {
                "brand_models": {
                    "Casio": ["G-Shock Classic"],
                    "Seiko": ["5 Sports Automatic"],
                    "Fossil": ["Grant Chronograph"],
                    "Tissot": ["PRX Powermatic 80"],
                    "Citizen": ["Eco-Drive Promaster"]
                },
                "images": ["1524805444758-089113d48a6d", "1549972352-7104fded7a30", "1622329618074-d4b9981ed73e"],
                "tags": ["watch", "timepiece", "analog", "wrist", "accessory"]
            },
            "Sunglasses": {
                "brand_models": {
                    "Ray-Ban": ["Classic Wayfarer"],
                    "Oakley": ["Holbrook"],
                    "Persol": ["714 Folding"],
                    "Prada": ["Linea Rossa"],
                    "Maui Jim": ["Peahi Polarized"]
                },
                "images": ["1511499767150-a48a237f0083", "1559564177-d0c3c8f8d689"],
                "tags": ["sunglasses", "eyewear", "summer", "uv-protection", "accessory"]
            },
            "Wallets": {
                "brand_models": {
                    "Bellroy": ["Note Sleeve"],
                    "Fossil": ["Derrick Bifold"],
                    "Tommy Hilfiger": ["Leather Passcase"],
                    "Secrid": ["Slim Wallet"],
                    "Timberland": ["Hunter Trifold"]
                },
                "images": ["1627123424574-724758594e93", "1548036328-c896dce5a7f8"],
                "tags": ["wallet", "leather", "slim", "rfid", "accessory"]
            },
            "Belts": {
                "brand_models": {
                    "Levi's": ["Reversible Leather Belt"],
                    "Calvin Klein": ["Classic Logo Belt"],
                    "Gucci": ["GG Marmont Belt"],
                    "Tommy Hilfiger": ["Stretch Belt"],
                    "Dickies": ["Web Belt"]
                },
                "images": ["1603808033192-082d6919d3e1", "1594938328870-c67e3d728f1f"],
                "tags": ["belt", "leather", "casual", "formal", "accessory"]
            }
        }
    },
    "Fitness": {
        "count": 100,
        "subcategories": {
            "Dumbbells": {
                "brand_models": {
                    "Bowflex": ["SelectTech 552"],
                    "CAP Barbell": ["Hex Dumbbell Set"],
                    "Rogue": ["Rubber Hex Dumbbells"],
                    "Amazon Basics": ["Neoprene Dumbbell"],
                    "Yes4All": ["Adjustable Dumbbells"]
                },
                "images": ["1534438327276-14e5300c3a48", "1571019613454-1cb2f99b2d8b", "1576678927484-cc907957088c", "1598971639058-feb753d2ee06"],
                "tags": ["dumbbells", "weights", "strength", "home-gym", "fitness"]
            },
            "Yoga Mats": {
                "brand_models": {
                    "Manduka": ["PRO Yoga Mat"],
                    "Lululemon": ["The Reversible Mat"],
                    "Gaiam": ["Premium Print Mat"],
                    "JadeYoga": ["Harmony Mat"],
                    "Alo Yoga": ["Warrior Mat"]
                },
                "images": ["1534438327276-14e5300c3a48", "1571019613454-1cb2f99b2d8b", "1576678927484-cc907957088c", "1598971639058-feb753d2ee06"],
                "tags": ["yoga", "mat", "stretching", "pilates", "fitness"]
            },
            "Resistance Bands": {
                "brand_models": {
                    "TheraBand": ["Professional Latex Bands"],
                    "Gritin": ["Resistance Loop Exercise Bands"],
                    "Fit Simplify": ["Set of 5 Bands"],
                    "Undersun": ["Fitness Bands"],
                    "SPRI": ["Xertube Resistance Band"]
                },
                "images": ["1534438327276-14e5300c3a48", "1571019613454-1cb2f99b2d8b", "1576678927484-cc907957088c", "1598971639058-feb753d2ee06"],
                "tags": ["resistance", "bands", "workout", "home-gym", "fitness"]
            },
            "Foam Rollers": {
                "brand_models": {
                    "TriggerPoint": ["GRID Foam Roller"],
                    "Amazon Basics": ["High-Density Foam Roller"],
                    "LuxFit": ["Speckled Foam Roller"],
                    "OPTP": ["Pro-Roller Standard"],
                    "Brazyn": ["Morph Collapsible Roller"]
                },
                "images": ["1534438327276-14e5300c3a48", "1571019613454-1cb2f99b2d8b", "1576678927484-cc907957088c", "1598971639058-feb753d2ee06"],
                "tags": ["recovery", "massage", "foam-roller", "stretching", "fitness"]
            },
            "Protein Shakers": {
                "brand_models": {
                    "BlenderBottle": ["Classic V2"],
                    "ShakeSphere": ["Tumbler"],
                    "Hydra Cup": ["Dual Shaker"],
                    "Helimix": ["Vortex Shaker"],
                    "Promixx": ["Pro Shaker"]
                },
                "images": ["1534438327276-14e5300c3a48", "1571019613454-1cb2f99b2d8b", "1576678927484-cc907957088c", "1598971639058-feb753d2ee06"],
                "tags": ["shaker", "protein", "bottle", "gym", "fitness"]
            },
             "Fitness Trackers": {
                "brand_models": {
                    "Fitbit": ["Charge 5"],
                    "Garmin": ["Vivosmart 5"],
                    "Xiaomi": ["Mi Band 7"],
                    "Amazfit": ["Band 7"],
                    "WHOOP": ["WHOOP 4.0"]
                },
                "images": ["1534438327276-14e5300c3a48", "1571019613454-1cb2f99b2d8b", "1576678927484-cc907957088c", "1598971639058-feb753d2ee06"],
                "tags": ["tracker", "wearable", "health", "steps", "fitness"]
            }
        }
    },
    "Sports": {
        "count": 100,
        "subcategories": {
            "Cricket": {
                "brand_models": {
                    "SG": ["Players Bat"],
                    "SS": ["Ton Gladiator"],
                    "Kookaburra": ["Kahuna Pro"],
                    "Gray-Nicolls": ["Vapor 1.0"],
                    "MRF": ["Genius Grand Edition"]
                },
                "images": ["1531415074968-036ba1b575da", "1579952363873-f5c7deff2e99", "1461896836934-ffe607ba8211"],
                "tags": ["cricket", "bat", "sports", "outdoor", "team"]
            },
            "Football": {
                "brand_models": {
                    "Nike": ["Flight Ball"],
                    "Adidas": ["Al Rihla Pro"],
                    "Puma": ["La Liga 1"],
                    "Mitre": ["Delta Professional"],
                    "Select": ["Brillant Super"]
                },
                "images": ["1531415074968-036ba1b575da", "1579952363873-f5c7deff2e99", "1461896836934-ffe607ba8211"],
                "tags": ["football", "soccer", "ball", "sports", "outdoor"]
            },
            "Basketball": {
                "brand_models": {
                    "Spalding": ["NBA Official Game Ball"],
                    "Wilson": ["Evolution Game Basketball"],
                    "Nike": ["Elite Championship"],
                    "Under Armour": ["495 Indoor"],
                    "Molten": ["BG5000"]
                },
                "images": ["1531415074968-036ba1b575da", "1579952363873-f5c7deff2e99", "1461896836934-ffe607ba8211"],
                "tags": ["basketball", "hoops", "sports", "indoor", "ball"]
            },
            "Tennis": {
                "brand_models": {
                    "Wilson": ["Pro Staff 97"],
                    "Babolat": ["Pure Drive"],
                    "HEAD": ["Radical MP"],
                    "Yonex": ["EZONE 98"],
                    "Prince": ["Phantom 100"]
                },
                "images": ["1531415074968-036ba1b575da", "1579952363873-f5c7deff2e99", "1461896836934-ffe607ba8211"],
                "tags": ["tennis", "racket", "sports", "outdoor", "court"]
            },
            "Badminton": {
                "brand_models": {
                    "Yonex": ["Astrox 99 Pro"],
                    "Victor": ["Thruster F"],
                    "Li-Ning": ["Aeronaut 9000"],
                    "Apacs": ["Z-Ziggler"],
                    "Carlton": ["Kinesis 80S"]
                },
                "images": ["1531415074968-036ba1b575da", "1579952363873-f5c7deff2e99", "1461896836934-ffe607ba8211"],
                "tags": ["badminton", "racket", "shuttlecock", "sports", "indoor"]
            }
        }
    },
    "Gaming": {
        "count": 100,
        "subcategories": {
            "Controllers": {
                "brand_models": {
                    "Sony": ["DualSense Wireless"],
                    "Microsoft": ["Xbox Elite Series 2"],
                    "Nintendo": ["Pro Controller"],
                    "Razer": ["Wolverine V2"],
                    "8BitDo": ["Ultimate Bluetooth"]
                },
                "images": ["1612287230202-1ff1d85d1bdf", "1593305841991-05c297ba4575", "1616588589676-62b3d4ff6e36"],
                "tags": ["controller", "gamepad", "gaming", "console", "pc"]
            },
            "Gaming Keyboards": {
                "brand_models": {
                    "Razer": ["Huntsman V2"],
                    "Corsair": ["K100 RGB"],
                    "SteelSeries": ["Apex Pro TKL"],
                    "Logitech G": ["G915 Lightspeed"],
                    "HyperX": ["Alloy Origins"]
                },
                "images": ["1612287230202-1ff1d85d1bdf", "1593305841991-05c297ba4575", "1616588589676-62b3d4ff6e36"],
                "tags": ["keyboard", "mechanical", "rgb", "gaming", "pc"]
            },
            "Gaming Mice": {
                "brand_models": {
                    "Logitech G": ["G Pro X Superlight"],
                    "Razer": ["DeathAdder V3 Pro"],
                    "SteelSeries": ["Aerox 5 Wireless"],
                    "Glorious": ["Model O"],
                    "Roccat": ["Kone Pro Air"]
                },
                "images": ["1612287230202-1ff1d85d1bdf", "1593305841991-05c297ba4575", "1616588589676-62b3d4ff6e36"],
                "tags": ["mouse", "gaming", "rgb", "wireless", "pc"]
            },
            "Headsets": {
                "brand_models": {
                    "HyperX": ["Cloud II Wireless"],
                    "SteelSeries": ["Arctis Nova Pro"],
                    "Razer": ["BlackShark V2 Pro"],
                    "Logitech G": ["PRO X Wireless"],
                    "Astro": ["A50 Wireless"]
                },
                "images": ["1612287230202-1ff1d85d1bdf", "1593305841991-05c297ba4575", "1616588589676-62b3d4ff6e36"],
                "tags": ["headset", "audio", "mic", "gaming", "surround"]
            },
            "Gaming Chairs": {
                "brand_models": {
                    "Secretlab": ["Titan Evo 2022"],
                    "Noblechairs": ["Hero Series"],
                    "Corsair": ["T3 Rush"],
                    "Razer": ["Iskur"],
                    "DXRacer": ["Formula Series"]
                },
                "images": ["1612287230202-1ff1d85d1bdf", "1593305841991-05c297ba4575", "1616588589676-62b3d4ff6e36"],
                "tags": ["chair", "ergonomic", "gaming", "comfort", "setup"]
            }
        }
    },
    "Home Appliances": {
        "count": 120,
        "subcategories": {
            "Kitchen": {
                "brand_models": {
                    "Instant Pot": ["Duo 7-in-1"],
                    "Ninja": ["Foodi Air Fryer"],
                    "Breville": ["Barista Express"],
                    "KitchenAid": ["Artisan Stand Mixer"],
                    "Philips": ["Essential Airfryer"]
                },
                "images": ["1585659722983-3a675dabf23d", "1556909114-f6e7ad7d3136", "1544568100-4c60e3220241"],
                "tags": ["kitchen", "cooking", "appliance", "home", "food"]
            },
            "Cleaning": {
                "brand_models": {
                    "Dyson": ["V15 Detect"],
                    "Shark": ["Navigator Lift-Away"],
                    "iRobot": ["Roomba j7+"],
                    "Bissell": ["CrossWave"],
                    "Miele": ["Complete C3"]
                },
                "images": ["1585659722983-3a675dabf23d", "1556909114-f6e7ad7d3136", "1544568100-4c60e3220241"],
                "tags": ["cleaning", "vacuum", "home", "appliance", "smart"]
            },
            "Coffee Makers": {
                "brand_models": {
                    "Keurig": ["K-Elite"],
                    "Nespresso": ["VertuoPlus"],
                    "Breville": ["Bambino Plus"],
                    "De'Longhi": ["Magnifica S"],
                    "Hamilton Beach": ["FlexBrew"]
                },
                "images": ["1585659722983-3a675dabf23d", "1556909114-f6e7ad7d3136", "1544568100-4c60e3220241"],
                "tags": ["coffee", "espresso", "morning", "kitchen", "appliance"]
            },
            "Air Purifiers": {
                "brand_models": {
                    "Coway": ["Airmega 400"],
                    "Levoit": ["Core 400S"],
                    "Dyson": ["Purifier Cool"],
                    "Winix": ["5500-2"],
                    "Blueair": ["Blue Pure 211+"]
                },
                "images": ["1585659722983-3a675dabf23d", "1556909114-f6e7ad7d3136", "1544568100-4c60e3220241"],
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
                brand = random.choice(list(subcat_data["brand_models"].keys()))
                model = random.choice(subcat_data["brand_models"][brand])
                
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
