import React, { useRef, useEffect, useMemo } from 'react';
import activityTracker from '../../services/activityTracker';

const CompareDropdown = ({ product, isOpen, onClose }) => {
    const ref = useRef(null);
    
    // Generate simulated competitors based on category
    const competitors = useMemo(() => {
        if (!product || !product.name) return [];
        
        const cat = product.category || '';
        const nameQuery = encodeURIComponent(product.name);
        const basePrice = product.price || 0;
        
        // Generate pseudo-random deterministic price variation (-5% to +5%)
        const getPrice = (seed) => {
            if (basePrice === 0) return 0;
            // Use product ID to make variations deterministic per product
            const variation = ((product.id * seed) % 10) / 100 - 0.05; 
            return (basePrice * (1 + variation)).toFixed(2);
        };
        
        const allCompetitors = {
            amazon: { name: 'Amazon', icon: '📦', url: `https://www.amazon.in/s?k=${nameQuery}`, color: 'text-[#FF9900]', price: getPrice(3) },
            flipkart: { name: 'Flipkart', icon: '🛒', url: `https://www.flipkart.com/search?q=${nameQuery}`, color: 'text-[#2874F0]', price: getPrice(7) },
            myntra: { name: 'Myntra', icon: '🛍️', url: `https://www.myntra.com/${nameQuery}`, color: 'text-[#FF3E6C]', price: getPrice(5) },
            bestbuy: { name: 'Best Buy', icon: '🏷️', url: `https://www.bestbuy.com/site/searchpage.jsp?st=${nameQuery}`, color: 'text-[#0046BE]', price: getPrice(11) },
            ajio: { name: 'Ajio', icon: '✨', url: `https://www.ajio.com/search/?text=${nameQuery}`, color: 'text-[#2C4152]', price: getPrice(13) }
        };
        
        const result = [];
        const cLower = cat.toLowerCase();
        
        if (cLower === 'electronics' || cLower === 'headphones' || cLower === 'laptop' || cLower === 'phone') {
            result.push(allCompetitors.amazon, allCompetitors.flipkart, allCompetitors.bestbuy);
        } else if (cLower === 'fashion' || cLower === 'bags' || cLower === 'shoes') {
            result.push(allCompetitors.myntra, allCompetitors.ajio, allCompetitors.amazon);
        } else if (cLower === 'accessories' || cLower === 'watches') {
            result.push(allCompetitors.amazon, allCompetitors.flipkart);
        } else {
            // Default generic fallback
            result.push(allCompetitors.amazon, allCompetitors.flipkart);
        }
        
        return result;
    }, [product]);

    useEffect(() => {
        const handleClickOutside = (e) => {
            if (ref.current && !ref.current.contains(e.target)) onClose();
        };
        if (isOpen) document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, [isOpen, onClose]);

    if (!isOpen) return null;

    return (
        <div ref={ref} className="absolute bottom-full left-0 right-0 mb-2 bg-white border-2 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] z-50 animate-fadeIn min-w-[200px]">
            <div className="px-3 py-2 border-b-2 border-black bg-gray-50 flex items-center justify-between">
                <p className="text-xs font-black uppercase tracking-widest text-gray-600">Compare Deals</p>
                <span className="text-[10px] font-bold text-gray-400">EXTERNAL</span>
            </div>
            <div className="divide-y divide-gray-100">
                {competitors.length > 0 ? (
                    competitors.map((entry) => (
                        <a
                            key={entry.name}
                            href={entry.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            onClick={() => {
                                activityTracker.trackCompareClick(product?.id, entry.name);
                                onClose();
                            }}
                            className="w-full flex items-center justify-between px-3 py-3 text-sm hover:bg-gray-50 transition-colors group"
                        >
                            <div className="flex items-center gap-2">
                                <span className="text-base">{entry.icon}</span>
                                <span className="font-bold text-gray-800">{entry.name}</span>
                            </div>
                            <div className="flex items-center gap-3">
                                {entry.price > 0 && (
                                    <span className="font-bold text-black">${entry.price}</span>
                                )}
                                <span className={`text-xs font-black uppercase tracking-wider ${entry.color}`}>Buy</span>
                                <span className="text-gray-400 group-hover:text-black transition-colors">↗</span>
                            </div>
                        </a>
                    ))
                ) : (
                    <div className="px-3 py-3 text-sm text-gray-500 font-medium">
                        No deals found.
                    </div>
                )}
            </div>
        </div>
    );
};

export default CompareDropdown;
