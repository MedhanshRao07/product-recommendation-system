import React, { useRef, useEffect } from 'react';
import activityTracker from '../../services/activityTracker';

const CompareDropdown = ({ product, isOpen, onClose }) => {
    const ref = useRef(null);
    
    // We get the real URLs from the product object
    const competitors = [];
    
    if (product?.amazon_url) {
        competitors.push({ name: 'Amazon', icon: '📦', url: product.amazon_url, color: 'text-[#FF9900]' });
    }
    if (product?.flipkart_url) {
        competitors.push({ name: 'Flipkart', icon: '🛒', url: product.flipkart_url, color: 'text-[#2874F0]' });
    }
    if (product?.myntra_url) {
        competitors.push({ name: 'Myntra', icon: '🛍️', url: product.myntra_url, color: 'text-[#FF3E6C]' });
    }

    useEffect(() => {
        const handleClickOutside = (e) => {
            if (ref.current && !ref.current.contains(e.target)) onClose();
        };
        if (isOpen) document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, [isOpen, onClose]);

    if (!isOpen) return null;

    return (
        <div ref={ref} className="absolute bottom-full left-0 right-0 mb-2 bg-white border-2 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] z-50 animate-fadeIn">
            <div className="px-3 py-2 border-b-2 border-black bg-gray-50 flex items-center justify-between">
                <p className="text-xs font-black uppercase tracking-widest text-gray-600">Compare Deals</p>
                <span className="text-[10px] font-bold text-gray-400">EXTERNAL LINK</span>
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
                            <div className="flex items-center gap-2">
                                <span className={`text-xs font-black uppercase tracking-wider ${entry.color}`}>Search</span>
                                <span className="text-gray-400 group-hover:text-black transition-colors">↗</span>
                            </div>
                        </a>
                    ))
                ) : (
                    <div className="px-3 py-3 text-sm text-gray-500 font-medium">
                        No external marketplace links available.
                    </div>
                )}
            </div>
        </div>
    );
};

export default CompareDropdown;
