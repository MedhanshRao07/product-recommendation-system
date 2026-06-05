import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'backend', '.env'))

# Explicit Keyword Mappings
TYPE_KEYWORDS = {
    'monitor': ['monitor', 'display', 'ultrasharp', 'proart', 'odyssey', 'screen'],
    'keyboard': ['keyboard', 'mechanical', 'mx mechanical', 'k70', 'k95', 'keypad'],
    'mouse': ['mouse', 'deathadder', 'g502', 'mx master', 'viper'],
    'speaker': ['speaker', 'charge', 'boombox', 'soundcore', 'homepod', 'echo'],
    'watch': ['watch', 'chronograph', 'prx', 'g-shock', 'smartwatch', 'apple watch'],
    'wallet': ['wallet', 'bifold', 'passcase', 'trifold'],
    'belt': ['belt', 'reversible belt', 'web belt'],
    'foam_roller': ['foam roller', 'roller'],
    'resistance_band': ['resistance band', 'band', 'loop'],
    'dumbbell': ['dumbbell', 'weights'],
    'laptop': ['laptop', 'macbook', 'xps', 'zenbook', 'matebook', 'spectre', 'thinkpad'],
    'charger': ['charger', 'adapter', 'power adapter', 'wall charger'],
    'cable': ['usb', 'hdmi', 'cable', 'extension'],
    'headphone': ['headphone', 'headphones', 'quietcomfort', 'wh-1000xm', 'over-ear', '660nc'],
    'earbud': ['earbud', 'earbuds', 'airpods', 'galaxy buds', 'in-ear'],
    'backpack': ['backpack', 'messenger', 'duffel', 'bag', 'timbuk2'],
    'shoe': ['shoe', 'sneaker', 'air force', 'air max', 'running'],
    'boot': ['boot', 'timberland', 'chelsea'],
    'tv': ['tv', 'television', 'oled', 'qled'],
    'phone': ['phone', 'iphone', 'galaxy s', 'smartphone'],
    'tablet': ['tablet', 'ipad', 'galaxy tab'],
    'sunglasses': ['sunglass', 'sunglasses', 'aviator', 'wayfarer', 'shades'],
    'camera': ['camera', 'eos', 'alpha', 'lumix'],
    'purifier': ['purifier', 'air purifier'],
    'fryer': ['fryer', 'air fryer'],
    'coffee': ['coffee', 'espresso', 'keurig', 'nespresso'],
    'kettle': ['kettle', 'electric kettle'],
    'cookware': ['cookware', 'pan', 'skillet', 'pot'],
    'shirt': ['shirt', 'polo', 'flannel', 't-shirt'],
    'sweater': ['sweater', 'hoodie', 'pullover', 'fleece', 'jacket'],
    'jeans': ['jeans', 'denim', 'pants'],
    'power_bank': ['power bank', 'portable charger']
}

# Strict Image Pools
POOLS = {
    'monitor': ['/images/products/monitor.png', '/images/products/acer_139_cm.jpg', '/images/products/vu_139_cm.jpg', '/images/products/monitor_v1.png', '/images/products/monitor_v2.png'],
    'keyboard': ['/images/products/keyboard1.png', '/images/products/keyboard_v1.png', '/images/products/keyboard_v2.png'],
    'mouse': ['/images/products/mouse.png', '/images/products/razer_deathadder_v3_pro_black.jpg', '/images/products/mouse_v1.png'],
    'speaker': ['/images/products/apple_homepod_mini_cosmic_grey.jpg', '/images/products/amazon_echo_plus.jpg', '/images/products/speaker_v1.png', '/images/products/speaker_v2.png'],
    'watch': ['/images/products/apple_watch_series_4_gold.jpg', '/images/products/rolex_submariner_watch.jpg', '/images/products/boat_wave_call_smart_watch.jpg', '/images/products/noise_colorfit_pro_4_advanced_bluetooth_calling_smart.jpg'],
    'wallet': ['/images/products/wallet1.png', '/images/products/wallet_v2.png'],
    'belt': ['/images/products/belt1.png', '/images/products/brown_leather_belt_watch.jpg'],
    'foam_roller': ['/images/products/foamroller1.png'],
    'resistance_band': ['/images/products/resistance_band_v1.png'],
    'dumbbell': ['/images/products/dumbbell_v1.png', '/images/products/dumbbell_v2.png'],
    'laptop': ['/images/products/macbook_pro_14.png', '/images/products/huawei_matebook_x_pro.jpg', '/images/products/new_dell_xps_13_9300_laptop.jpg', '/images/products/asus_zenbook_pro_dual_screen_laptop.jpg', '/images/products/laptop_v1.png', '/images/products/laptop_v2.png'],
    'charger': ['/images/products/apple_iphone_charger.jpg', '/images/products/samsung_25w_usb_travel_adapter_for_cellular_phones.jpg', '/images/products/ptron_bullet_pro_36w_pd_quick_charger.jpg'],
    'cable': ['/images/products/amazonbasics_usb_2_0_extension_cable_for_personal_computer.jpg', '/images/products/boat_micro_usb_55_tangle.jpg', '/images/products/wayona_usb_type_c_65w_fast_charging_2m_6ft.jpg'],
    'headphone': ['/images/products/sony_headphones.png', '/images/products/apple_airpods_max_silver.jpg'],
    'earbud': ['/images/products/apple_airpods.jpg', '/images/products/samsung_galaxy_buds_live_bluetooth_truly_wireless_in.jpg'],
    'backpack': ['/images/products/backpack1.png', '/images/products/white_faux_leather_backpack.jpg', '/images/products/timbuk2_classic_messenger_bag_jet_black.jpg'],
    'shoe': ['/images/products/nike_air_force.png', '/images/products/new_balance.png', '/images/products/nike_air_max_270_black.jpg'],
    'boot': ['/images/products/timberland_boot.png'],
    'tv': ['/images/products/tv1.png', '/images/products/lg_c3_series_55_inch_oled_tv_black.jpg'],
    'phone': ['/images/products/iphone_15_pro.png', '/images/products/galaxy_s24_ultra.png', '/images/products/iphone_13_pro.jpg', '/images/products/samsung_galaxy_s10.jpg'],
    'tablet': ['/images/products/ipad_mini_2021_starlight.jpg', '/images/products/samsung_galaxy_tab_s8_plus_grey.jpg'],
    'sunglasses': ['/images/products/sunglasses.jpg', '/images/products/black_sun_glasses.jpg', '/images/products/classic_sun_glasses.jpg'],
    'camera': ['/images/products/canon_eos_r5.png'],
    'purifier': ['/images/products/purifier.png'],
    'fryer': ['/images/products/airfryer.png'],
    'coffee': ['/images/products/coffeemaker.png'],
    'kettle': ['/images/products/kettle.png'],
    'cookware': ['/images/products/cookware.png'],
    'shirt': ['/images/products/shirt1.png'],
    'sweater': ['/images/products/patagonia_sweater.png'],
    'jeans': ['/images/products/shirt1.png'],
    'power_bank': ['/images/products/powerbank1.png']
}

def detect_product_type(name):
    s_name = name.lower()
    for p_type, keywords in TYPE_KEYWORDS.items():
        for kw in keywords:
            if kw in s_name:
                return p_type
    return None

def get_image(name, cat, pid):
    p_type = detect_product_type(name)
    
    if p_type and p_type in POOLS:
        pool = POOLS[p_type]
        return p_type, pool[pid % len(pool)]
        
    # Absolute generic fallback (only used if NO type matched)
    # Ensure it's safe for the broad category
    category = cat.lower()
    if 'fashion' in category:
        return 'generic_fashion', '/images/products/shirt1.png'
    elif 'home' in category:
        return 'generic_home', '/images/products/coffeemaker.png'
    elif 'fitness' in category or 'sports' in category:
        return 'generic_fitness', '/images/products/foamroller1.png'
    elif 'shoes' in category:
        return 'generic_shoes', '/images/products/nike_air_force.png'
    elif 'bags' in category:
        return 'generic_bags', '/images/products/backpack1.png'
    elif 'accessories' in category:
        return 'generic_accessories', '/images/products/rolex_submariner.png'
    
    # Do NOT map unrecognized electronics to generic cables
    if 'electronics' in category or 'gaming' in category:
        return 'generic_electronics', '/images/products/macbook_pro_14.png'

    return 'unknown', '/images/products/backpack1.png'

def run():
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST', '127.0.0.1'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'suggestify_db')
    )
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute('SELECT id, name, category, image_url FROM products')
    products = cursor.fetchall()
    
    updates = 0
    print("=== PRODUCT CLASSIFICATION ASSIGNMENTS ===")
    for p in products:
        p_type, new_url = get_image(p['name'], p['category'], p['id'])
        
        # Debug logging as requested
        print(f"{p['name']}")
        print(f"-> type={p_type}")
        print(f"-> pool={p_type}")
        print(f"-> image={new_url.split('/')[-1]}")
        print("---")
        
        if new_url != p['image_url']:
            cursor.execute('UPDATE products SET image_url = %s WHERE id = %s', (new_url, p['id']))
            updates += 1
            
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Successfully remapped {updates} product images.")

if __name__ == '__main__':
    run()
