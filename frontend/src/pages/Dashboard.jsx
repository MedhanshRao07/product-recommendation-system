import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import authService from '../services/authService';
import ProductCard from '../components/products/ProductCard';
import activityTracker from '../services/activityTracker';

const CATEGORY_ICONS = {
    'Electronics': '💻', 'Clothing': '👕', 'Shoes': '👟',
    'Accessories': '⌚', 'Home & Kitchen': '🏠', 'Sports & Outdoors': '⚽',
};

const Dashboard = () => {
    const [user, setUser] = useState(null);
    const [trending, setTrending] = useState([]);
    const [recommendations, setRecommendations] = useState([]);
    const [groupedProducts, setGroupedProducts] = useState({});
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [trendingRes, groupedRes] = await Promise.all([
                    axios.get('http://localhost:5000/trending'),
                    axios.get('http://localhost:5000/api/products/grouped?per_category=6'),
                ]);
                setTrending(trendingRes.data || []);
                setGroupedProducts(groupedRes.data || {});

                // Fetch user data + recommendations
                try {
                    const currentUser = await authService.getCurrentUser();
                    setUser(currentUser);
                    if (currentUser && currentUser.id) {
                        const recRes = await axios.get(`http://localhost:5000/api/products/auto-recommend/${currentUser.id}`);
                        if (recRes.data && recRes.data.recommendations) {
                            setRecommendations(recRes.data.recommendations);
                        }
                    }
                } catch (e) {
                    // Not logged in — that's fine
                }
            } catch (err) {
                console.error('Failed to load dashboard data', err);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    if (loading) {
        return (
            <div className="min-h-screen bg-white flex items-center justify-center">
                <div className="flex flex-col items-center gap-3">
                    <div className="animate-spin rounded-full h-10 w-10 border-2 border-black border-t-transparent"></div>
                    <p className="text-sm font-bold text-gray-400 uppercase tracking-widest">Loading...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-white text-black selection:bg-black selection:text-white">
            
            {/* ═══ Hero Section ═══ */}
            <div className="relative min-h-[85vh] flex flex-col justify-center overflow-hidden bg-[#fafafa] pt-16">
                {/* Background typography */}
                <div className="absolute inset-0 flex items-center justify-center pointer-events-none select-none z-0 opacity-[0.04]">
                    <h1 className="text-[40vw] font-black tracking-tighter leading-none text-black">S</h1>
                </div>

                <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
                    <div className="max-w-2xl">
                        <p className="text-xs font-bold uppercase tracking-[0.3em] text-[#ed7844] mb-4">AI-Powered Shopping</p>
                        <h2 className="text-5xl sm:text-6xl lg:text-7xl font-black tracking-tight uppercase leading-[0.9] mb-6">
                            Discover
                            <br />
                            <span className="text-[#ed7844]">your</span> perfect
                            <br />
                            match<span className="text-[#ed7844]">.</span>
                        </h2>
                        <p className="text-base sm:text-lg text-gray-600 mb-10 max-w-lg font-medium leading-relaxed">
                            Suggestify uses intelligent recommendations to curate products tailored to your unique tastes and preferences.
                        </p>
                        <div className="flex flex-wrap gap-4">
                            <button
                                onClick={() => navigate('/products')}
                                className="group relative inline-flex items-center"
                            >
                                <span className="relative z-10 px-8 py-3.5 bg-black text-white text-sm font-bold uppercase tracking-widest border-2 border-black group-hover:bg-[#ed7844] group-hover:border-[#ed7844] transition-colors duration-300">
                                    Shop Now
                                </span>
                            </button>
                            {user && (
                                <button
                                    onClick={() => navigate('/recommendations')}
                                    className="px-8 py-3.5 text-sm font-bold uppercase tracking-widest border-2 border-black text-black hover:bg-black hover:text-white transition-colors duration-300"
                                >
                                    My Recommendations
                                </button>
                            )}
                        </div>
                    </div>
                </div>

                {/* Scroll indicator */}
                <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 animate-bounce">
                    <span className="text-[10px] font-bold uppercase tracking-widest text-gray-400">Scroll</span>
                    <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
                    </svg>
                </div>
            </div>

            {/* ═══ Recommended For You (logged in only) ═══ */}
            {recommendations.length > 0 && (
                <section className="py-16 bg-black text-white">
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <div className="flex items-center justify-between mb-10">
                            <div>
                                <p className="text-xs font-bold uppercase tracking-[0.3em] text-[#ed7844] mb-2">Personalized</p>
                                <h2 className="text-3xl font-black uppercase tracking-tight">
                                    Recommended For You
                                </h2>
                            </div>
                            <button
                                onClick={() => navigate('/recommendations')}
                                className="hidden sm:block text-xs font-bold uppercase tracking-wider text-[#ed7844] border border-[#ed7844] px-4 py-2 hover:bg-[#ed7844] hover:text-black transition-colors"
                            >
                                View All →
                            </button>
                        </div>
                        <div className="flex gap-4 overflow-x-auto pb-4 scrollbar-hide snap-x snap-mandatory">
                            {recommendations.map((product) => (
                                <div key={`rec-${product.id}`} className="w-64 flex-shrink-0 snap-start"
                                     onClick={() => activityTracker.trackRecommendationClick(product.id)}>
                                    <ProductCard product={product} />
                                </div>
                            ))}
                        </div>
                    </div>
                </section>
            )}

            {/* ═══ Trending Now ═══ */}
            {trending.length > 0 && (
                <section className="py-16 bg-[#fafafa]">
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <div className="flex items-center justify-between mb-10">
                            <div>
                                <p className="text-xs font-bold uppercase tracking-[0.3em] text-gray-400 mb-2">Top Rated</p>
                                <h2 className="text-3xl font-black uppercase tracking-tight text-black">Trending Now</h2>
                            </div>
                        </div>
                        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4 sm:gap-6">
                            {trending.slice(0, 8).map((product) => (
                                <ProductCard key={`trending-${product.id}`} product={product} />
                            ))}
                        </div>
                    </div>
                </section>
            )}

            {/* ═══ Category Sections ═══ */}
            <section className="py-16 bg-white">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="mb-12">
                        <p className="text-xs font-bold uppercase tracking-[0.3em] text-gray-400 mb-2">Browse</p>
                        <h2 className="text-3xl font-black uppercase tracking-tight text-black">Shop by Category</h2>
                    </div>
                    
                    <div className="space-y-12">
                        {Object.entries(groupedProducts).map(([category, prods]) => (
                            <div key={category}>
                                <div className="flex items-center justify-between mb-6">
                                    <h3 className="text-lg font-black uppercase tracking-tight flex items-center gap-2">
                                        <span className="text-xl">{CATEGORY_ICONS[category] || '📦'}</span>
                                        {category}
                                    </h3>
                                    <button
                                        onClick={() => navigate(`/products?category=${encodeURIComponent(category)}`)}
                                        className="text-xs font-bold uppercase tracking-wider text-[#ed7844] hover:text-black transition-colors"
                                    >
                                        View All →
                                    </button>
                                </div>
                                <div className="flex gap-4 overflow-x-auto pb-4 scrollbar-hide snap-x snap-mandatory">
                                    {prods.map((product) => (
                                        <div key={product.id} className="w-64 flex-shrink-0 snap-start">
                                            <ProductCard product={product} />
                                        </div>
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* ═══ CTA Footer ═══ */}
            <section className="py-20 bg-black text-white text-center">
                <div className="max-w-2xl mx-auto px-4">
                    <h2 className="text-3xl sm:text-4xl font-black uppercase tracking-tight mb-4">
                        Ready to find your next favorite?
                    </h2>
                    <p className="text-gray-400 mb-8 font-medium">
                        Join thousands of users who discover products they love with Suggestify.
                    </p>
                    {!user ? (
                        <button
                            onClick={() => navigate('/register')}
                            className="px-10 py-4 bg-[#ed7844] text-black text-sm font-bold uppercase tracking-widest border-2 border-[#ed7844] hover:bg-transparent hover:text-[#ed7844] transition-colors duration-300"
                        >
                            Get Started Free
                        </button>
                    ) : (
                        <button
                            onClick={() => navigate('/products')}
                            className="px-10 py-4 bg-[#ed7844] text-black text-sm font-bold uppercase tracking-widest border-2 border-[#ed7844] hover:bg-transparent hover:text-[#ed7844] transition-colors duration-300"
                        >
                            Continue Shopping
                        </button>
                    )}
                </div>
            </section>
        </div>
    );
};

export default Dashboard;
