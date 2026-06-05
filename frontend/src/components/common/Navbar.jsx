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
            <nav className={`fixed w-full top-0 z-50 transition-all duration-300 border-b-2 border-black ${
                scrolled 
                    ? 'bg-white/70 backdrop-blur-md shadow-sm' 
                    : 'bg-white/95 backdrop-blur-sm'
            }`}>
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex items-center justify-between h-20">

                        {/* Logo */}
                        <Link to="/dashboard" className="font-black text-2xl tracking-tighter text-black uppercase flex-shrink-0 hover:opacity-70 transition-opacity">
                            SUGGESTIFY<span className="text-[#ed7844]">.</span>
                        </Link>

                        {/* Desktop Nav Links */}
                        <div className="hidden lg:flex items-center space-x-10">
                            <Link to="/dashboard" className="relative group text-sm font-extrabold tracking-widest uppercase text-black">
                                Home
                                <span className="absolute -bottom-1.5 left-0 w-0 h-0.5 bg-[#ed7844] transition-all duration-300 ease-[cubic-bezier(0.25,1,0.5,1)] group-hover:w-full"></span>
                            </Link>

                            {/* Categories Dropdown */}
                            <div className="relative" ref={catRef}>
                                <button 
                                    onClick={() => setShowCategories(!showCategories)}
                                    className="relative group text-sm font-extrabold tracking-widest uppercase text-black flex items-center gap-1"
                                >
                                    Categories
                                    <svg className={`w-4 h-4 transition-transform duration-300 ${showCategories ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M19 9l-7 7-7-7" />
                                    </svg>
                                    <span className="absolute -bottom-1.5 left-0 w-0 h-0.5 bg-[#ed7844] transition-all duration-300 ease-[cubic-bezier(0.25,1,0.5,1)] group-hover:w-full"></span>
                                </button>
                                {showCategories && (
                                    <div className="absolute top-[120%] left-0 mt-2 w-56 bg-white border-2 border-black shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] py-2 z-50 animate-[fadeInSlideDown_0.2s_ease-out_forwards] opacity-0 origin-top">
                                        {categories.map(cat => (
                                            <button 
                                                key={cat}
                                                onClick={() => handleCategoryClick(cat)}
                                                className="w-full text-left px-5 py-3 text-xs font-bold uppercase tracking-widest text-gray-700 hover:bg-black hover:text-white transition-colors duration-200"
                                            >
                                                {cat}
                                            </button>
                                        ))}
                                    </div>
                                )}
                            </div>

                            <Link to="/products" className="relative group text-sm font-extrabold tracking-widest uppercase text-black">
                                Products
                                <span className="absolute -bottom-1.5 left-0 w-0 h-0.5 bg-[#ed7844] transition-all duration-300 ease-[cubic-bezier(0.25,1,0.5,1)] group-hover:w-full"></span>
                            </Link>

                            {isLoggedIn && (
                                <Link to="/recommendations" className="relative group text-sm font-extrabold tracking-widest uppercase text-black">
                                    Recommendations
                                    <span className="absolute -bottom-1.5 left-0 w-0 h-0.5 bg-[#ed7844] transition-all duration-300 ease-[cubic-bezier(0.25,1,0.5,1)] group-hover:w-full"></span>
                                </Link>
                            )}
                        </div>

                        {/* Right Side: Search + Cart + User */}
                        <div className="flex items-center space-x-6">
                            {/* Search */}
                            <div className="relative" ref={searchRef}>
                                {showSearch ? (
                                    <form onSubmit={handleSearch} className="flex items-center animate-fadeIn">
                                        <input
                                            type="text"
                                            value={searchQuery}
                                            onChange={(e) => setSearchQuery(e.target.value)}
                                            placeholder="Search products..."
                                            autoFocus
                                            className="w-48 sm:w-64 px-4 py-2 text-sm font-bold uppercase tracking-wider border-2 border-black focus:outline-none focus:ring-0 bg-white placeholder-gray-400"
                                        />
                                        <button type="button" onClick={() => { setShowSearch(false); setSearchQuery(''); }} className="ml-2 p-2 text-black hover:text-[#ed7844] transition-colors">
                                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M6 18L18 6M6 6l12 12"/></svg>
                                        </button>
                                    </form>
                                ) : (
                                    <button onClick={() => setShowSearch(true)} className="p-2 text-black hover:text-[#ed7844] transition-colors" aria-label="Search">
                                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                                        </svg>
                                    </button>
                                )}
                            </div>

                            {/* Cart */}
                            <Link to="/cart" className="relative p-2 text-black hover:text-[#ed7844] transition-colors group">
                                <svg className="w-6 h-6 transform group-hover:scale-110 transition-transform duration-300 ease-[cubic-bezier(0.25,1,0.5,1)]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                                </svg>
                                {cartItemCount > 0 && (
                                    <span className="absolute -top-1 -right-1 bg-[#ed7844] text-white text-[10px] font-black w-5 h-5 flex items-center justify-center rounded-full border-2 border-black">
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
                                            className="p-2 text-black hover:text-[#ed7844] transition-colors"
                                        >
                                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                            </svg>
                                        </button>
                                        {showUserMenu && (
                                            <div className="absolute right-0 top-[120%] mt-2 w-56 bg-white border-2 border-black shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] py-2 z-50 animate-[fadeInSlideDown_0.2s_ease-out_forwards] opacity-0 origin-top">
                                                <Link to="/preferences" onClick={() => setShowUserMenu(false)} className="block px-5 py-3 text-xs font-bold uppercase tracking-widest text-gray-700 hover:bg-black hover:text-white transition-colors duration-200">
                                                    Preferences
                                                </Link>
                                                <button onClick={handleLogout} className="w-full text-left px-5 py-3 text-xs font-bold uppercase tracking-widest text-gray-700 hover:bg-black hover:text-white transition-colors duration-200">
                                                    Logout
                                                </button>
                                            </div>
                                        )}
                                    </>
                                ) : (
                                    <div className="flex items-center space-x-6">
                                        <Link to="/login" className="relative group text-sm font-extrabold uppercase tracking-widest text-black">
                                            Log in
                                            <span className="absolute -bottom-1.5 left-0 w-0 h-0.5 bg-black transition-all duration-300 ease-[cubic-bezier(0.25,1,0.5,1)] group-hover:w-full"></span>
                                        </Link>
                                        <Link to="/register" className="px-6 py-2.5 bg-black text-white text-sm font-extrabold uppercase tracking-widest border-2 border-black hover:bg-white hover:text-black hover:shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] transition-all duration-300">
                                            Sign up
                                        </Link>
                                    </div>
                                )}
                            </div>

                            {/* Mobile Hamburger */}
                            <button
                                onClick={() => setShowMobileMenu(!showMobileMenu)}
                                className="lg:hidden p-2 text-black hover:text-[#ed7844] transition-colors"
                                aria-label="Menu"
                            >
                                {showMobileMenu ? (
                                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M6 18L18 6M6 6l12 12" /></svg>
                                ) : (
                                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M4 6h16M4 12h16M4 18h16" /></svg>
                                )}
                            </button>
                        </div>
                    </div>
                </div>
            </nav>

            {/* Mobile Menu Drawer */}
            {showMobileMenu && (
                <div className="fixed inset-0 z-40 lg:hidden">
                    <div className="absolute inset-0 bg-black/50 backdrop-blur-sm animate-fadeIn" onClick={() => setShowMobileMenu(false)} />
                    <div className="absolute right-0 top-0 h-full w-80 bg-white border-l-4 border-black shadow-[0_0_40px_rgba(0,0,0,0.5)] overflow-y-auto animate-[slideInRight_0.3s_ease-out_forwards]">
                        <div className="pt-24 px-8 pb-8 space-y-2">
                            {/* Search in mobile */}
                            <form onSubmit={handleSearch} className="mb-8">
                                <input
                                    type="text"
                                    value={searchQuery}
                                    onChange={(e) => setSearchQuery(e.target.value)}
                                    placeholder="SEARCH..."
                                    className="w-full px-4 py-3 text-sm font-bold uppercase tracking-widest border-2 border-black focus:outline-none focus:ring-0 bg-gray-50"
                                />
                            </form>

                            <Link to="/dashboard" onClick={() => setShowMobileMenu(false)} className="block py-4 text-sm font-extrabold uppercase tracking-widest text-black border-b-2 border-black/10">Home</Link>
                            <Link to="/products" onClick={() => setShowMobileMenu(false)} className="block py-4 text-sm font-extrabold uppercase tracking-widest text-black border-b-2 border-black/10">All Products</Link>

                            {/* Categories */}
                            <div className="py-4 border-b-2 border-black/10">
                                <p className="text-[10px] font-black text-[#ed7844] uppercase tracking-[0.2em] mb-4">Categories</p>
                                <div className="space-y-3">
                                    {categories.map(cat => (
                                        <button key={cat} onClick={() => handleCategoryClick(cat)} className="block w-full text-left py-1 text-sm font-bold text-gray-600 hover:text-black uppercase tracking-wider">
                                            {cat}
                                        </button>
                                    ))}
                                </div>
                            </div>

                            {isLoggedIn ? (
                                <div className="pt-2">
                                    <Link to="/recommendations" onClick={() => setShowMobileMenu(false)} className="block py-4 text-sm font-extrabold uppercase tracking-widest text-black border-b-2 border-black/10">Recommendations</Link>
                                    <Link to="/preferences" onClick={() => setShowMobileMenu(false)} className="block py-4 text-sm font-extrabold uppercase tracking-widest text-black border-b-2 border-black/10">Preferences</Link>
                                    <button onClick={() => { handleLogout(); setShowMobileMenu(false); }} className="block w-full text-left py-4 text-sm font-extrabold uppercase tracking-widest text-red-600 hover:text-red-800 transition-colors">Logout</button>
                                </div>
                            ) : (
                                <div className="pt-6 space-y-4">
                                    <Link to="/login" onClick={() => setShowMobileMenu(false)} className="block w-full text-center py-3 text-sm font-extrabold uppercase tracking-widest text-black border-2 border-black">Log in</Link>
                                    <Link to="/register" onClick={() => setShowMobileMenu(false)} className="block w-full text-center py-3 text-sm font-extrabold uppercase tracking-widest bg-[#ed7844] text-black border-2 border-black">Sign up</Link>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            )}
        </>
    );
};

export default Navbar;
