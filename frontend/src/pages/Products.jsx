import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import ProductCard from '../components/products/ProductCard';
import activityTracker from '../services/activityTracker';

const CATEGORY_ICONS = {
    'Electronics': '💻',
    'Clothing': '👕',
    'Shoes': '👟',
    'Accessories': '⌚',
    'Home & Kitchen': '🏠',
    'Sports & Outdoors': '⚽',
};

const Products = () => {
    const [products, setProducts] = useState([]);
    const [groupedProducts, setGroupedProducts] = useState({});
    const [categories, setCategories] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();

    const activeCategory = searchParams.get('category') || 'All';
    const searchQuery = searchParams.get('search') || '';

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                if (searchQuery) {
                    // Search mode
                    activityTracker.trackSearch(searchQuery);
                    const res = await axios.get(`${process.env.REACT_APP_API_URL || 'http://localhost:5000'}/api/products/search?q=${encodeURIComponent(searchQuery)}`);
                    setProducts(res.data || []);
                    setGroupedProducts({});
                } else if (activeCategory !== 'All') {
                    // Single category
                    activityTracker.trackCategoryVisit(activeCategory);
                    const res = await axios.get(`${process.env.REACT_APP_API_URL || 'http://localhost:5000'}/api/products/category/${encodeURIComponent(activeCategory)}`);
                    setProducts(res.data || []);
                    setGroupedProducts({});
                } else {
                    // All categories — grouped view
                    const res = await axios.get(`${process.env.REACT_APP_API_URL || 'http://localhost:5000'}/api/products/grouped?per_category=8`);
                    setGroupedProducts(res.data || {});
                    setProducts([]);
                }
                // Fetch categories for pills
                const catRes = await axios.get(`${process.env.REACT_APP_API_URL || 'http://localhost:5000'}/api/products/categories`);
                setCategories(catRes.data || []);
            } catch (error) {
                console.error("Error fetching products:", error);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [activeCategory, searchQuery]);

    const handleCategoryChange = (cat) => {
        if (cat === 'All') {
            navigate('/products');
        } else {
            navigate(`/products?category=${encodeURIComponent(cat)}`);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-[#fafafa] flex items-center justify-center pt-16">
                <div className="flex flex-col items-center gap-3">
                    <div className="animate-spin rounded-full h-10 w-10 border-2 border-black border-t-transparent"></div>
                    <p className="text-sm font-bold text-gray-400 uppercase tracking-widest">Loading products...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-[#fafafa] pt-20 pb-16 text-black">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

                {/* Page Header */}
                <div className="pt-8 pb-6">
                    {searchQuery ? (
                        <div>
                            <h1 className="text-3xl font-black uppercase tracking-tight">
                                Search: "{searchQuery}"
                            </h1>
                            <p className="text-sm text-gray-500 mt-1 font-medium">{products.length} results found</p>
                        </div>
                    ) : (
                        <h1 className="text-3xl font-black uppercase tracking-tight">
                            {activeCategory === 'All' ? 'Shop by Category' : activeCategory}
                        </h1>
                    )}
                </div>

                {/* Category Pills */}
                {!searchQuery && (
                    <div className="flex flex-wrap gap-2 mb-8 pb-6 border-b-2 border-gray-200">
                        <button
                            onClick={() => handleCategoryChange('All')}
                            className={`px-4 py-2 text-xs font-bold uppercase tracking-wider border-2 transition-all duration-200 ${
                                activeCategory === 'All'
                                    ? 'bg-black text-white border-black'
                                    : 'bg-white text-gray-600 border-gray-200 hover:border-black hover:text-black'
                            }`}
                        >
                            All
                        </button>
                        {categories.map(cat => (
                            <button
                                key={cat}
                                onClick={() => handleCategoryChange(cat)}
                                className={`px-4 py-2 text-xs font-bold uppercase tracking-wider border-2 transition-all duration-200 flex items-center gap-1.5 ${
                                    activeCategory === cat
                                        ? 'bg-black text-white border-black'
                                        : 'bg-white text-gray-600 border-gray-200 hover:border-black hover:text-black'
                                }`}
                            >
                                <span>{CATEGORY_ICONS[cat] || '📦'}</span>
                                {cat}
                            </button>
                        ))}
                    </div>
                )}

                {/* Content */}
                {searchQuery || activeCategory !== 'All' ? (
                    /* Grid view for search or single category */
                    products.length === 0 ? (
                        <div className="text-center py-20">
                            <p className="text-xl font-bold text-gray-400">No products found</p>
                            <button onClick={() => navigate('/products')} className="mt-4 px-6 py-2 border-2 border-black font-bold text-sm uppercase hover:bg-black hover:text-white transition-colors">
                                View All Products
                            </button>
                        </div>
                    ) : (
                        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4 sm:gap-6">
                            {products.map((product) => (
                                <ProductCard key={product.id} product={product} />
                            ))}
                        </div>
                    )
                ) : (
                    /* Grouped category sections */
                    <div className="space-y-12">
                        {Object.entries(groupedProducts).map(([category, prods]) => (
                            <section key={category}>
                                <div className="flex items-center justify-between mb-6">
                                    <h2 className="text-xl font-black uppercase tracking-tight flex items-center gap-2">
                                        <span className="text-2xl">{CATEGORY_ICONS[category] || '📦'}</span>
                                        {category}
                                        <span className="text-xs font-bold text-gray-400 ml-2">({prods.length})</span>
                                    </h2>
                                    <button
                                        onClick={() => handleCategoryChange(category)}
                                        className="text-xs font-bold uppercase tracking-wider text-[#ed7844] hover:text-black border-b-2 border-transparent hover:border-black transition-all pb-0.5"
                                    >
                                        View All →
                                    </button>
                                </div>
                                {/* Horizontal scroll row */}
                                <div className="flex gap-4 overflow-x-auto pb-4 scrollbar-hide snap-x snap-mandatory">
                                    {prods.map((product) => (
                                        <div key={product.id} className="w-64 flex-shrink-0 snap-start">
                                            <ProductCard product={product} />
                                        </div>
                                    ))}
                                </div>
                            </section>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default Products;
