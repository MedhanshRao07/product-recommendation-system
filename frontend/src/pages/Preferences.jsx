import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ProductCard from '../components/products/ProductCard';

const Preferences = () => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const response = await axios.get(`${process.env.REACT_APP_API_URL || 'http://localhost:5000'}/api/products`);
                const data = response.data;
                const productsArray = Array.isArray(data) ? data : (data.products || []);
                setProducts(productsArray);
            } catch (err) {
                console.error('Failed to load products', err);
            } finally {
                setLoading(false);
            }
        };

        fetchProducts();
    }, []);

    if (loading) {
        return (
            <div className="min-h-screen bg-white flex items-center justify-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-black"></div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-[#f4f4f4] text-black py-24 px-8 md:px-16 selection:bg-black selection:text-white mt-8">
            <h1 className="text-5xl md:text-6xl font-black uppercase tracking-tighter mb-16 border-b-8 border-black pb-6">Explore Products</h1>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
                {products.map((product) => (
                    <ProductCard key={product.id} product={product} />
                ))}
            </div>
        </div>
    );
};

export default Preferences;
