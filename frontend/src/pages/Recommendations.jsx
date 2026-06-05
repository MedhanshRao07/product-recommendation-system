import React, { useState, useEffect } from 'react';
import { useLocation, Link } from 'react-router-dom';
import axios from 'axios';
import ProductCard from '../components/products/ProductCard';
import activityTracker from '../services/activityTracker';
import authService from '../services/authService';

const Recommendations = () => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const location = useLocation();

    useEffect(() => {
        const fetchRecommendations = async () => {
            try {
                const currentUser = await authService.getCurrentUser();
                let response;
                
                if (currentUser && currentUser.id) {
                    response = await axios.get(`http://localhost:5000/api/products/auto-recommend/${currentUser.id}`);
                } else {
                    response = await axios.get('http://localhost:5000/api/products');
                }

                if (response.data && response.data.recommendations) {
                    setProducts(response.data.recommendations);
                } else if (Array.isArray(response.data)) {
                    // Fallback trending returns array directly
                    setProducts(response.data.slice(0, 12));
                } else {
                    setProducts([]);
                }
            } catch (err) {
                console.error("Error fetching recommendations:", err);
                setError('Failed to fetch recommendations. Please try again later.');
            } finally {
                setLoading(false);
            }
        };

        fetchRecommendations();
    }, [location.search]);

    if (loading) {
        return (
            <div className="min-h-screen bg-[#fafafa] pt-20 pb-16">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8">
                    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8 animate-pulse">
                        <div>
                            <div className="h-3 w-24 bg-gray-200 mb-3 rounded"></div>
                            <div className="h-8 w-64 bg-gray-300 mb-2 rounded"></div>
                            <div className="h-4 w-96 bg-gray-200 rounded"></div>
                        </div>
                    </div>
                    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4 sm:gap-6">
                        {[...Array(8)].map((_, i) => (
                            <div key={i} className="border-2 border-gray-100 bg-white flex flex-col h-[400px] animate-pulse">
                                <div className="aspect-square bg-gray-200 w-full"></div>
                                <div className="p-4 flex flex-col flex-grow">
                                    <div className="h-2 w-16 bg-gray-200 mb-3 rounded"></div>
                                    <div className="h-4 w-3/4 bg-gray-300 mb-2 rounded"></div>
                                    <div className="h-4 w-1/2 bg-gray-200 mb-6 rounded"></div>
                                    <div className="mt-auto pt-3 border-t border-gray-100 flex justify-between items-center">
                                        <div className="h-6 w-16 bg-gray-300 rounded"></div>
                                        <div className="flex gap-2 w-1/2">
                                            <div className="h-8 w-full bg-gray-200 rounded"></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen bg-[#fafafa] pt-20 px-4">
                <div className="max-w-lg mx-auto mt-20 bg-white border-2 border-black p-8 text-center">
                    <p className="text-xl font-black uppercase mb-2">Oops!</p>
                    <p className="text-gray-500 mb-6 font-medium">{error}</p>
                    <Link to="/preferences" className="px-6 py-2 border-2 border-black text-sm font-bold uppercase tracking-widest hover:bg-black hover:text-white transition-colors">
                        Go back to preferences
                    </Link>
                </div>
            </div>
        );
    }

    if (products.length === 0) {
        return (
            <div className="min-h-screen bg-[#fafafa] pt-20 px-4">
                <div className="max-w-lg mx-auto mt-20 bg-white border-2 border-black p-8 text-center">
                    <p className="text-xl font-black uppercase mb-2">No Matches Found</p>
                    <p className="text-gray-500 mb-6 font-medium">
                        We couldn't find any recommendations yet. Explore our products to help us learn your tastes.
                    </p>
                    <Link to="/preferences" className="px-6 py-2 border-2 border-black text-sm font-bold uppercase tracking-widest hover:bg-black hover:text-white transition-colors">
                        Explore Products
                    </Link>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-[#fafafa] pt-20 pb-16 text-black">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8">
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8">
                    <div>
                        <p className="text-xs font-bold uppercase tracking-[0.3em] text-[#ed7844] mb-1">Intelligently Curated</p>
                        <h1 className="text-3xl font-black uppercase tracking-tight">Your Smart Picks</h1>
                        <p className="mt-1 text-sm text-gray-500 font-medium">Dynamically updated based on your recent views, similar tastes, and trending items.</p>
                    </div>
                    <Link
                        to="/preferences"
                        className="mt-4 sm:mt-0 text-xs font-bold uppercase tracking-wider text-gray-500 hover:text-black border border-gray-300 hover:border-black px-4 py-2 transition-all"
                    >
                        Explore More →
                    </Link>
                </div>

                <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4 sm:gap-6">
                    {products.map((product, index) => (
                        <div key={index} onClick={() => activityTracker.trackRecommendationClick(product.id)}>
                            <ProductCard product={product} />
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default Recommendations;
