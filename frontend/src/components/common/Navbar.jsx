import React, { useState, useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { isAuthenticated } from '../../utils/auth';
import authService from '../../services/authService';
import { useCart } from '../../context/CartContext';
import activityTracker from '../../services/activityTracker';
import axios from 'axios';

const Navbar = () => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [showSearch, setShowSearch] = useState(false);
    const [searchQuery, setSearchQuery] = useState('');
    const [showCategories, setShowCategories] = useState(false);
    const [showMobileMenu, setShowMobileMenu] = useState(false);
    const [showUserMenu, setShowUserMenu] = useState(false);
    const [categories, setCategories] = useState([]);
    const [scrolled, setScrolled] = useState(false);
    const navigate = useNavigate();
    const { cartItemCount } = useCart();
    const catRef = useRef(null);
    const userRef = useRef(null);
    const searchRef = useRef(null);

    useEffect(() => {
        setIsLoggedIn(isAuthenticated());
        const handleAuthChange = () => setIsLoggedIn(isAuthenticated());
        window.addEventListener('authChange', handleAuthChange);

        // Fetch categories
        axios.get('http://localhost:5000/api/products/categories')
            .then(res => setCategories(res.data || []))
            .catch(() => {});

        // Scroll listener
        const handleScroll = () => setScrolled(window.scrollY > 20);
        window.addEventListener('scroll', handleScroll);

        // Close dropdowns on outside click
        const handleClickOutside = (e) => {
            if (catRef.current && !catRef.current.contains(e.target)) setShowCategories(false);
            if (userRef.current && !userRef.current.contains(e.target)) setShowUserMenu(false);
        };
        document.addEventListener('mousedown', handleClickOutside);

        return () => {
            window.removeEventListener('authChange', handleAuthChange);
            window.removeEventListener('scroll', handleScroll);
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, []);

    const handleSearch = (e) => {
        e.preventDefault();
        if (searchQuery.trim()) {
            activityTracker.trackSearch(searchQuery.trim());
            navigate(`/products?search=${encodeURIComponent(searchQuery.trim())}`);
            setSearchQuery('');
            setShowSearch(false);
            setShowMobileMenu(false);
        }
    };

    const handleLogout = () => {
        authService.logout();
        setShowUserMenu(false);
        navigate('/login');
    };

    const handleCategoryClick = (cat) => {
        activityTracker.trackCategoryVisit(cat);
        setShowCategories(false);
        setShowMobileMenu(false);
        navigate(`/products?category=${encodeURIComponent(cat)}`);
    };

    return (
        <>
            <nav className={`fixed w-full top-0 z-50 transition-all duration-300 ${
                scrolled 
                    ? 'bg-white/95 backdrop-blur-md shadow-md border-b border-gray-200' 
                    : 'bg-white border-b border-gray-200'
            }`}>
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex items-center justify-between h-16">

                        {/* Logo */}
                        <Link to="/dashboard" className="font-extrabold text-xl tracking-tighter text-black uppercase flex-shrink-0 hover:opacity-70 transition-opacity">
                            SUGGESTIFY<span className="text-[#ed7844]">.</span>
                        </Link>

                        {/* Desktop Nav Links */}
                        <div className="hidden lg:flex items-center space-x-6">
                            <Link to="/dashboard" className="text-sm font-bold tracking-wide text-gray-700 hover:text-black transition-colors">
                                Home
                            </Link>

                            {/* Categories Dropdown */}
                            <div className="relative" ref={catRef}>
                                <button 
                                    onClick={() => setShowCategories(!showCategories)}
                                    className="text-sm font-bold tracking-wide text-gray-700 hover:text-black transition-colors flex items-center gap-1"
                                >
                                    Categories
                                    <svg className={`w-3.5 h-3.5 transition-transform ${showCategories ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M19 9l-7 7-7-7" />
                                    </svg>
                                </button>
                                {showCategories && (
                                    <div className="absolute top-full left-0 mt-2 w-56 bg-white border-2 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] py-1 z-50">
                                        {categories.map(cat => (
                                            <button 
                                                key={cat}
                                                onClick={() => handleCategoryClick(cat)}
                                                className="w-full text-left px-4 py-2.5 text-sm font-semibold text-gray-700 hover:bg-black hover:text-white transition-colors"
                                            >
                                                {cat}
                                            </button>
                                        ))}
                                    </div>
                                )}
                            </div>

                            <Link to="/products" className="text-sm font-bold tracking-wide text-gray-700 hover:text-black transition-colors">
                                Products
                            </Link>

                            {isLoggedIn && (
                                <Link to="/recommendations" className="text-sm font-bold tracking-wide text-gray-700 hover:text-black transition-colors">
                                    Recommendations
                                </Link>
                            )}
                        </div>

                        {/* Right Side: Search + Cart + User */}
                        <div className="flex items-center space-x-3">
                            {/* Search */}
                            <div className="relative" ref={searchRef}>
                                {showSearch ? (
                                    <form onSubmit={handleSearch} className="flex items-center">
                                        <input
                                            type="text"
                                            value={searchQuery}
                                            onChange={(e) => setSearchQuery(e.target.value)}
                                            placeholder="Search products..."
                                            autoFocus
                                            className="w-40 sm:w-56 px-3 py-1.5 text-sm border-2 border-black focus:outline-none focus:ring-0 font-medium"
                                        />
                                        <button type="button" onClick={() => { setShowSearch(false); setSearchQuery(''); }} className="ml-1 p-1.5 text-gray-400 hover:text-black">
                                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"/></svg>
                                        </button>
                                    </form>
                                ) : (
                                    <button onClick={() => setShowSearch(true)} className="p-2 text-gray-600 hover:text-black transition-colors" aria-label="Search">
                                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                                        </svg>
                                    </button>
                                )}
                            </div>

                            {/* Cart */}
                            <Link to="/cart" className="relative p-2 text-gray-600 hover:text-black transition-colors group">
                                <svg className="w-5 h-5 transform group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                                </svg>
                                {cartItemCount > 0 && (
                                    <span className="absolute -top-0.5 -right-0.5 bg-[#ed7844] text-white text-xs font-black w-5 h-5 flex items-center justify-center rounded-full border border-black">
                                        {cartItemCount > 9 ? '9+' : cartItemCount}
                                    </span>
                                )}
                            </Link>

                            {/* User Menu */}
                            <div className="relative hidden lg:block" ref={userRef}>
                                {isLoggedIn ? (
                                    <>
                                        <button
                                            onClick={() => setShowUserMenu(!showUserMenu)}
                                            className="p-2 text-gray-600 hover:text-black transition-colors"
                                        >
                                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                            </svg>
                                        </button>
                                        {showUserMenu && (
                                            <div className="absolute right-0 top-full mt-2 w-48 bg-white border-2 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] py-1 z-50">
                                                <Link to="/preferences" onClick={() => setShowUserMenu(false)} className="block px-4 py-2.5 text-sm font-semibold text-gray-700 hover:bg-black hover:text-white transition-colors">
                                                    Preferences
                                                </Link>
                                                <button onClick={handleLogout} className="w-full text-left px-4 py-2.5 text-sm font-semibold text-gray-700 hover:bg-black hover:text-white transition-colors">
                                                    Logout
                                                </button>
                                            </div>
                                        )}
                                    </>
                                ) : (
                                    <div className="flex items-center space-x-3">
                                        <Link to="/login" className="text-sm font-bold text-gray-700 hover:text-black transition-colors">
                                            Log in
                                        </Link>
                                        <Link to="/register" className="relative inline-block text-sm font-bold text-black hover:text-white group">
                                            <span className="relative z-10 px-4 py-1.5 block">Sign up</span>
                                            <div className="absolute inset-0 bg-[#ed7844] transform -skew-x-12 z-0 transition-transform group-hover:scale-105"></div>
                                        </Link>
                                    </div>
                                )}
                            </div>

                            {/* Mobile Hamburger */}
                            <button
                                onClick={() => setShowMobileMenu(!showMobileMenu)}
                                className="lg:hidden p-2 text-gray-600 hover:text-black transition-colors"
                                aria-label="Menu"
                            >
                                {showMobileMenu ? (
                                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" /></svg>
                                ) : (
                                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" /></svg>
                                )}
                            </button>
                        </div>
                    </div>
                </div>
            </nav>

            {/* Mobile Menu Drawer */}
            {showMobileMenu && (
                <div className="fixed inset-0 z-40 lg:hidden">
                    <div className="absolute inset-0 bg-black/50" onClick={() => setShowMobileMenu(false)} />
                    <div className="absolute right-0 top-0 h-full w-72 bg-white border-l-4 border-black shadow-xl overflow-y-auto">
                        <div className="pt-20 px-6 pb-8 space-y-1">
                            {/* Search in mobile */}
                            <form onSubmit={handleSearch} className="mb-6">
                                <input
                                    type="text"
                                    value={searchQuery}
                                    onChange={(e) => setSearchQuery(e.target.value)}
                                    placeholder="Search..."
                                    className="w-full px-3 py-2 text-sm border-2 border-black focus:outline-none font-medium"
                                />
                            </form>

                            <Link to="/dashboard" onClick={() => setShowMobileMenu(false)} className="block py-3 text-base font-bold text-black border-b border-gray-100">Home</Link>
                            <Link to="/products" onClick={() => setShowMobileMenu(false)} className="block py-3 text-base font-bold text-black border-b border-gray-100">All Products</Link>

                            {/* Categories */}
                            <div className="py-3 border-b border-gray-100">
                                <p className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-2">Categories</p>
                                {categories.map(cat => (
                                    <button key={cat} onClick={() => handleCategoryClick(cat)} className="block w-full text-left py-2 pl-3 text-sm font-semibold text-gray-600 hover:text-black">
                                        {cat}
                                    </button>
                                ))}
                            </div>

                            {isLoggedIn ? (
                                <>
                                    <Link to="/recommendations" onClick={() => setShowMobileMenu(false)} className="block py-3 text-base font-bold text-black border-b border-gray-100">Recommendations</Link>
                                    <Link to="/preferences" onClick={() => setShowMobileMenu(false)} className="block py-3 text-base font-bold text-black border-b border-gray-100">Preferences</Link>
                                    <button onClick={() => { handleLogout(); setShowMobileMenu(false); }} className="block w-full text-left py-3 text-base font-bold text-red-600">Logout</button>
                                </>
                            ) : (
                                <>
                                    <Link to="/login" onClick={() => setShowMobileMenu(false)} className="block py-3 text-base font-bold text-black border-b border-gray-100">Log in</Link>
                                    <Link to="/register" onClick={() => setShowMobileMenu(false)} className="block py-3 text-base font-bold text-[#ed7844]">Sign up</Link>
                                </>
                            )}
                        </div>
                    </div>
                </div>
            )}
        </>
    );
};

export default Navbar;
