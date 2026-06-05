import React, { useState, memo } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCart } from '../../context/CartContext';
import SafeImage from '../common/SafeImage';
import CompareDropdown from './CompareDropdown';
import activityTracker from '../../services/activityTracker';

// Star rating component
const Stars = memo(({ rating }) => {
    const full = Math.floor(rating || 0);
    const half = (rating || 0) - full >= 0.5;
    const empty = 5 - full - (half ? 1 : 0);
    return (
        <div className="flex items-center gap-0.5">
            {[...Array(full)].map((_, i) => (
                <svg key={`f${i}`} className="w-3 h-3 text-[#ed7844]" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
            ))}
            {half && (
                <svg className="w-3 h-3 text-[#ed7844]" fill="currentColor" viewBox="0 0 20 20">
                    <defs><clipPath id="halfClip"><rect x="0" y="0" width="10" height="20"/></clipPath></defs>
                    <path clipPath="url(#halfClip)" d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                    <path fill="#e5e7eb" d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
            )}
            {[...Array(empty)].map((_, i) => (
                <svg key={`e${i}`} className="w-3 h-3 text-gray-200" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
            ))}
            <span className="ml-1 text-[10px] font-bold text-gray-400">{(rating || 0).toFixed(1)}</span>
        </div>
    );
});

const ProductCard = memo(({ product }) => {
    const navigate = useNavigate();
    const { addToCart } = useCart();
    const [showCompare, setShowCompare] = useState(false);
    const [addedToCart, setAddedToCart] = useState(false);

    const handleAddToCart = (e) => {
        e.stopPropagation();
        addToCart(product);
        activityTracker.trackAddToCart(product.id);
        setAddedToCart(true);
        setTimeout(() => setAddedToCart(false), 1500);
    };

    const handleCompareToggle = (e) => {
        e.stopPropagation();
        setShowCompare(!showCompare);
    };

    const handleCardClick = () => {
        activityTracker.trackClick(product.id);
        navigate(`/product/${product.id}`);
    };

    return (
        <div
            onClick={handleCardClick}
            className="group relative border-2 border-gray-200 bg-white overflow-hidden transition-all duration-300 ease-out hover:border-black hover:shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] hover:-translate-y-1 flex flex-col h-full cursor-pointer"
        >
            {/* Category badge */}
            {product.category && (
                <div className="absolute top-3 left-3 z-10 bg-black text-white text-[10px] font-bold uppercase tracking-wider px-2 py-0.5">
                    {product.category}
                </div>
            )}

            {/* Recommendation badge */}
            {product.recommendation_reason && (
                <div className="absolute top-3 right-3 z-10 bg-white border-2 border-black text-black text-[9px] font-bold uppercase tracking-wider px-2 py-0.5 shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] flex items-center gap-1 max-w-[60%] text-right leading-tight">
                    <span className="text-[#ed7844]">✦</span>
                    {product.recommendation_reason}
                </div>
            )}

            {/* Image Container */}
            <div className="overflow-hidden border-b border-gray-100 bg-gray-50 p-4">
                <SafeImage 
                    src={product.image_url} 
                    alt={product.name} 
                    category={product.category}
                    productName={product.name}
                    className="aspect-square w-full object-contain mix-blend-multiply transition-opacity duration-300 group-hover:opacity-90"
                />
            </div>

            {/* Info */}
            <div className="p-4 flex flex-col flex-grow bg-white">
                <p className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1">
                    {product.brand}
                </p>
                <h3 className="text-sm font-bold tracking-tight text-black mb-2 line-clamp-2 leading-snug min-h-[2.5rem]">
                    {product.name}
                </h3>
                
                <Stars rating={product.rating} />

                <div className="mt-auto pt-3 border-t border-gray-100">
                    <div className="flex items-center justify-between mb-3">
                        <span className="text-lg font-black text-black">${product.price?.toFixed(2) || '0.00'}</span>
                    </div>

                    {/* Action buttons */}
                    <div className="relative flex gap-2">
                        <button
                            onClick={handleAddToCart}
                            className={`flex-1 px-3 py-2 text-xs font-bold uppercase tracking-wider border-2 transition-colors duration-200 ${
                                addedToCart 
                                    ? 'bg-black text-white border-black' 
                                    : 'bg-white text-black border-black hover:bg-black hover:text-white'
                            }`}
                        >
                            {addedToCart ? '✓ Added' : 'Add to Cart'}
                        </button>
                        <button
                            onClick={handleCompareToggle}
                            className={`px-2.5 py-2 text-xs font-bold border-2 transition-colors duration-200 ${
                                showCompare 
                                    ? 'bg-black text-white border-black' 
                                    : 'border-gray-300 text-gray-500 hover:border-black hover:text-black bg-white'
                            }`}
                            title="Compare Prices"
                        >
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                            </svg>
                        </button>
                        <CompareDropdown 
                            product={product}
                            isOpen={showCompare}
                            onClose={() => setShowCompare(false)}
                        />
                    </div>
                </div>
            </div>
        </div>
    );
});

export default ProductCard;
