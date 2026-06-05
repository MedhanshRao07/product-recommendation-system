import React, { useState, useEffect, useRef } from 'react';

const getFallbackImage = (category, name) => {
    const s_name = (name || '').toLowerCase();
    
    // 1. Exact Product Type Match
    if (s_name.includes('keyboard')) return '/images/products/keyboard1.png';
    if (s_name.includes('mouse')) return '/images/products/mouse.png';
    if (s_name.includes('monitor')) return '/images/products/monitor.png';
    if (s_name.includes('macbook')) return '/images/products/macbook_pro_14.png';
    if (s_name.includes('laptop')) return '/images/products/new_dell_xps_13_9300_laptop.jpg';
    if (s_name.includes('smartwatch')) return '/images/products/apple_watch_series_4_gold.jpg';
    if (s_name.includes('watch')) return '/images/products/rolex_submariner.png';
    if (s_name.includes('charger')) return '/images/products/apple_iphone_charger.jpg';
    if (s_name.includes('cable')) return '/images/products/amazonbasics_usb_2_0_extension_cable_for_personal_computer.jpg';
    if (s_name.includes('speaker')) return '/images/products/apple_homepod_mini_cosmic_grey.jpg';
    if (s_name.includes('headphone') || s_name.includes('660nc') || s_name.includes('quietcomfort') || s_name.includes('wh-1000xm')) return '/images/products/sony_headphones.png';
    if (s_name.includes('earbud') || s_name.includes('airpod')) return '/images/products/apple_airpods.jpg';
    if (s_name.includes('backpack') || s_name.includes('bag') || s_name.includes('duffel')) return '/images/products/backpack1.png';
    if (s_name.includes('shoe') || s_name.includes('sneaker')) return '/images/products/nike_air_force.png';
    if (s_name.includes('boot')) return '/images/products/timberland_boot.png';
    if (s_name.includes('foam roller') || s_name.includes('band') || s_name.includes('dumbbell') || s_name.includes('mat')) return '/images/products/foamroller1.png';
    if (s_name.includes('bottle') || s_name.includes('shaker')) return '/images/products/bottle1.png';
    if (s_name.includes('tv') || s_name.includes('television')) return '/images/products/tv1.png';
    if (s_name.includes('phone') || s_name.includes('iphone') || s_name.includes('galaxy')) return '/images/products/iphone_15_pro.png';
    if (s_name.includes('tablet')) return '/images/products/ipad_mini_2021_starlight.jpg';
    if (s_name.includes('sunglasses')) return '/images/products/sunglasses.jpg';
    if (s_name.includes('camera')) return '/images/products/canon_eos_r5.png';
    if (s_name.includes('purifier')) return '/images/products/purifier.png';
    if (s_name.includes('fryer')) return '/images/products/airfryer.png';
    if (s_name.includes('coffee')) return '/images/products/coffeemaker.png';
    if (s_name.includes('kettle')) return '/images/products/kettle.png';
    if (s_name.includes('cookware')) return '/images/products/cookware.png';
    if (s_name.includes('wallet')) return '/images/products/wallet1.png';
    if (s_name.includes('belt')) return '/images/products/belt1.png';
    if (s_name.includes('shirt') || s_name.includes('jeans') || s_name.includes('dress') || s_name.includes('polo')) return '/images/products/shirt1.png';
    if (s_name.includes('sweater') || s_name.includes('hoodie') || s_name.includes('jacket')) return '/images/products/patagonia_sweater.png';
    if (s_name.includes('power bank')) return '/images/products/powerbank1.png';
    
    // 2. Category Fallbacks (Prevent cross-contamination)
    const cat = (category || '').toLowerCase();
    if (cat.includes('electronics') || cat.includes('gaming')) return '/images/products/amazonbasics_usb_2_0_extension_cable_for_personal_computer.jpg';
    if (cat.includes('fashion') || cat.includes('clothing')) return '/images/products/shirt1.png';
    if (cat.includes('home')) return '/images/products/coffeemaker.png';
    if (cat.includes('fitness') || cat.includes('sports')) return '/images/products/foamroller1.png';
    if (cat.includes('shoes')) return '/images/products/nike_air_force.png';
    if (cat.includes('bags')) return '/images/products/backpack1.png';
    if (cat.includes('accessories')) return '/images/products/rolex_submariner.png';
    
    // 3. Absolute Fallback
    return '/images/products/backpack1.png';
};

const SafeImage = ({ src, alt, category, productName, className = '' }) => {
    const [imageState, setImageState] = useState('loading');
    const [currentSrc, setCurrentSrc] = useState(src);
    const imgRef = useRef(null);

    useEffect(() => {
        if (!src || src === 'url' || src === 'url_here' || (!src.startsWith('http') && !src.startsWith('/'))) {
            setCurrentSrc(getFallbackImage(category, productName));
            return;
        }
        
        setCurrentSrc(src);
        setImageState('loading');
        
        // If the image is instantly loaded from cache before onLoad can fire
        if (imgRef.current && imgRef.current.complete) {
            if (imgRef.current.naturalWidth > 0) {
                setImageState('loaded');
            }
        }
    }, [src, category, productName]);

    const handleLoad = () => {
        setImageState('loaded');
    };

    const handleError = () => {
        console.warn(`[SafeImage] Failed to load image asset: ${currentSrc}`);
        const fallback = getFallbackImage(category, productName);
        if (currentSrc !== fallback) {
            setCurrentSrc(fallback);
            setImageState('loading');
        } else {
            setImageState('loaded');
        }
    };

    return (
        <div className={`relative overflow-hidden bg-white flex-shrink-0 ${className}`}>
            {imageState === 'loading' && (
                <div className="absolute inset-0 animate-pulse bg-gray-200 z-0"></div>
            )}
            
            <img
                ref={imgRef}
                src={currentSrc}
                alt={alt}
                loading="lazy"
                onLoad={handleLoad}
                onError={handleError}
                className={`absolute inset-0 h-full w-full object-contain object-center transition-all duration-500 bg-white z-10 ${
                    imageState === 'loaded' ? 'opacity-100 group-hover:scale-105' : 'opacity-0'
                }`}
            />
        </div>
    );
};

export default SafeImage;
