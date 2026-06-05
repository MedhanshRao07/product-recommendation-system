import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useCart } from '../context/CartContext';
import ProductCard from '../components/products/ProductCard';
import CompareDropdown from '../components/products/CompareDropdown';
import activityTracker from '../services/activityTracker';

const ProductDetail = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [product, setProduct] = useState(null);
    const [relatedProducts, setRelatedProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const { addToCart } = useCart();
    const [added, setAdded] = useState(false);
    const [showCompare, setShowCompare] = useState(false);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                const response = await axios.get(`http://localhost:5000/product/${id}`);
                const prod = response.data.product || response.data;
                setProduct(prod);
                
                // Track view
                activityTracker.trackView(id);

                // Fetch related products
                const relRes = await axios.get(`http://localhost:5000/api/products/related/${id}`);
                setRelatedProducts(relRes.data || []);
            } catch (error) {
                console.error("Error fetching product details:", error);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [id]);

    const handleAddToCart = () => {
        if (product) {
            addToCart(product);
            activityTracker.trackAddToCart(product.id);
            setAdded(true);
            setTimeout(() => setAdded(false), 2000);
        }
    };

    // Star rating component
    const Stars = ({ rating, size = 'w-5 h-5' }) => {
        const full = Math.floor(rating || 0);
        const empty = 5 - full;
        return (
            <div className="flex items-center gap-0.5">
                {[...Array(full)].map((_, i) => (
                    <svg key={`f${i}`} className={`${size} text-[#ed7844]`} fill="currentColor" viewBox="0 0 20 20">
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                    </svg>
                ))}
                {[...Array(empty)].map((_, i) => (
                    <svg key={`e${i}`} className={`${size} text-gray-200`} fill="currentColor" viewBox="0 0 20 20">
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                    </svg>
                ))}
                <span className="ml-2 text-sm font-bold text-gray-500">{(rating || 0).toFixed(1)}</span>
            </div>
        );
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-[#fafafa] flex items-center justify-center pt-16">
                <div className="animate-spin rounded-full h-10 w-10 border-2 border-black border-t-transparent"></div>
            </div>
        );
    }

    if (!product) {
        return (
            <div className="min-h-screen bg-[#fafafa] flex flex-col items-center justify-center px-8 pt-16">
                <h2 className="text-3xl font-black uppercase mb-4">Product Not Found</h2>
                <button onClick={() => navigate('/products')} className="px-6 py-2 border-2 border-black font-bold text-sm uppercase hover:bg-black hover:text-white transition-colors">
                    Back to Products
                </button>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-[#fafafa] pt-20 pb-16 text-black">
            <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pt-8">

                {/* Breadcrumb */}
                <button
                    onClick={() => navigate(-1)}
                    className="mb-6 font-bold text-gray-400 hover:text-black transition-colors uppercase tracking-widest text-xs flex items-center gap-1 group"
                >
                    <span className="transform group-hover:-translate-x-1 transition-transform">←</span> Back
                </button>

                <div className="flex flex-col lg:flex-row gap-8 lg:gap-12 bg-white border border-gray-200 p-6 sm:p-8 lg:p-10">

                    {/* Product Image */}
                    <div className="w-full lg:w-1/2 flex-shrink-0 bg-gray-50 overflow-hidden relative">
                        {product.image_url && product.image_url !== 'url' && product.image_url !== 'url_here' ? (
                            <img src={product.image_url} alt={product.name} className="w-full h-auto aspect-square object-cover" loading="lazy" />
                        ) : (
                            <div className="w-full aspect-square flex items-center justify-center text-gray-300">
                                <span className="font-bold uppercase tracking-widest">No Image</span>
                            </div>
                        )}
                        {/* Category badge */}
                        <div className="absolute top-4 left-4 bg-black/80 text-white text-xs font-bold uppercase tracking-wider px-3 py-1">
                            {product.category}
                        </div>
                    </div>

                    {/* Product Info */}
                    <div className="w-full lg:w-1/2 flex flex-col">
                        <p className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-2">{product.brand}</p>
                        <h1 className="text-2xl sm:text-3xl font-black tracking-tight text-black mb-4 uppercase leading-tight">
                            {product.name}
                        </h1>
                        
                        <Stars rating={product.rating} />

                        <p className="text-3xl font-black text-black mt-4 mb-6">
                            ${product.price?.toFixed(2) || '0.00'}
                        </p>

                        <div className="border-t border-gray-100 pt-6 mb-8">
                            <h3 className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-3">Description</h3>
                            <p className="text-gray-600 leading-relaxed font-medium text-sm">
                                {product.description || "No description available for this product."}
                            </p>
                        </div>

                        {/* Actions */}
                        <div className="mt-auto space-y-3">
                            <button
                                onClick={handleAddToCart}
                                className={`w-full py-3.5 text-sm font-bold uppercase tracking-widest border-2 transition-all duration-300 ${
                                    added 
                                        ? 'bg-black text-white border-black' 
                                        : 'bg-[#ed7844] text-black border-black hover:bg-black hover:text-white'
                                }`}
                            >
                                {added ? '✓ Added to Cart' : 'Add to Cart'}
                            </button>
                            
                            {/* Compare Prices */}
                            <div className="relative">
                                <button
                                    onClick={() => setShowCompare(!showCompare)}
                                    className="w-full py-3 text-xs font-bold uppercase tracking-widest border border-gray-200 text-gray-600 hover:border-black hover:text-black transition-all flex items-center justify-center gap-2"
                                >
                                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                                    </svg>
                                    Compare Prices
                                </button>
                                <CompareDropdown product={product} isOpen={showCompare} onClose={() => setShowCompare(false)} />
                            </div>
                        </div>
                    </div>
                </div>

                {/* Related Products */}
                {relatedProducts.length > 0 && (
                    <section className="mt-16">
                        <h2 className="text-xl font-black uppercase tracking-tight mb-6">You Might Also Like</h2>
                        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4">
                            {relatedProducts.map((prod) => (
                                <ProductCard key={prod.id} product={prod} />
                            ))}
                        </div>
                    </section>
                )}
            </div>
        </div>
    );
};

export default ProductDetail;
