import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import authService from '../../services/authService';

const Register = () => {
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: '',
        confirmPassword: ''
    });

    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const validateForm = () => {
        if (!formData.name || !formData.email || !formData.password || !formData.confirmPassword) {
            return "All fields are required.";
        }
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(formData.email)) {
            return "Please enter a valid email address.";
        }
        if (formData.password.length < 6) {
            return "Password must be at least 6 characters long.";
        }
        if (formData.password !== formData.confirmPassword) {
            return "Passwords do not match.";
        }
        return null;
    };

    const handleRegister = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');
        setSuccess('');

        const validationError = validateForm();
        if (validationError) {
            setError(validationError);
            setIsLoading(false);
            return;
        }

        try {
            await authService.register(formData.name, formData.email, formData.password);
            setSuccess('Account created! Redirecting...');
            setFormData({ name: '', email: '', password: '', confirmPassword: '' });
            setTimeout(() => {
                navigate('/login');
            }, 2000);
        } catch (err) {
            if (err.response && err.response.data && err.response.data.error) {
                setError(err.response.data.error);
            } else {
                setError('Something went wrong during registration.');
            }
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex bg-[#f4f4f4]">
            {/* LEFT SIDE: Premium Branding */}
            <div className="hidden lg:flex lg:w-1/2 bg-[#0A0A0A] p-12 flex-col justify-between relative overflow-hidden border-r-2 border-black">
                {/* Subtle Grid Texture */}
                <div className="absolute inset-0 opacity-[0.03]" style={{ backgroundImage: 'linear-gradient(#fff 1px, transparent 1px), linear-gradient(90deg, #fff 1px, transparent 1px)', backgroundSize: '40px 40px' }}></div>
                
                <div className="relative z-10">
                    <Link to="/dashboard" className="font-black text-3xl tracking-tighter text-white uppercase hover:opacity-80 transition-opacity">
                        SUGGESTIFY<span className="text-[#ed7844]">.</span>
                    </Link>
                </div>

                <div className="relative z-10 max-w-lg mb-20">
                    <h1 className="text-5xl font-black text-white uppercase tracking-tight leading-[1.1] mb-6">
                        Join the future of ecommerce.
                    </h1>
                    <p className="text-gray-400 text-lg font-medium leading-relaxed mb-10">
                        Create an account to save your preferences and unlock a personalized shopping journey.
                    </p>
                    <div className="space-y-5">
                        <div className="flex items-center gap-4 text-gray-300 font-bold text-sm tracking-wide uppercase">
                            <span className="w-6 h-6 rounded-full bg-[#ed7844]/20 text-[#ed7844] flex items-center justify-center border border-[#ed7844]/50">✓</span> Save your wishlist
                        </div>
                        <div className="flex items-center gap-4 text-gray-300 font-bold text-sm tracking-wide uppercase">
                            <span className="w-6 h-6 rounded-full bg-[#ed7844]/20 text-[#ed7844] flex items-center justify-center border border-[#ed7844]/50">✓</span> Track your orders
                        </div>
                        <div className="flex items-center gap-4 text-gray-300 font-bold text-sm tracking-wide uppercase">
                            <span className="w-6 h-6 rounded-full bg-[#ed7844]/20 text-[#ed7844] flex items-center justify-center border border-[#ed7844]/50">✓</span> Get smarter recommendations
                        </div>
                    </div>
                </div>
            </div>

            {/* RIGHT SIDE: Auth Card */}
            <div className="w-full lg:w-1/2 flex items-center justify-center p-4 sm:p-6 lg:p-8 animate-fadeIn duration-500">
                <div className="max-w-md w-full space-y-8 bg-white p-10 border-2 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] mt-16 lg:mt-0">
                    <div>
                        <h2 className="mt-2 text-center text-4xl font-black tracking-tight text-black uppercase">
                            Create an Account
                        </h2>
                        <p className="mt-3 text-center text-sm text-gray-600 font-medium">
                            Sign up to get started.
                        </p>
                    </div>

                    {error && (
                        <div className="bg-red-50 text-red-500 p-4 border-2 border-red-500 text-sm font-bold text-center">
                            {error}
                        </div>
                    )}
                    {success && (
                        <div className="bg-emerald-50 text-emerald-600 p-4 border-2 border-emerald-500 text-sm font-bold text-center">
                            {success}
                        </div>
                    )}

                    <form className="mt-8 space-y-5" onSubmit={handleRegister}>
                        <div className="space-y-5">
                            <div>
                                <label className="block text-xs font-bold leading-6 text-black mb-2 uppercase tracking-widest">
                                    Name
                                </label>
                                <input
                                    name="name"
                                    type="text"
                                    required
                                    value={formData.name}
                                    onChange={handleChange}
                                    className="block w-full border-2 border-black py-3 px-4 text-black outline-none focus:ring-0 focus:border-[#ed7844] sm:text-sm transition-colors duration-200 bg-white"
                                />
                            </div>

                            <div>
                                <label className="block text-xs font-bold leading-6 text-black mb-2 uppercase tracking-widest">
                                    Email
                                </label>
                                <input
                                    name="email"
                                    type="email"
                                    required
                                    value={formData.email}
                                    onChange={handleChange}
                                    className="block w-full border-2 border-black py-3 px-4 text-black outline-none focus:ring-0 focus:border-[#ed7844] sm:text-sm transition-colors duration-200 bg-white"
                                />
                            </div>

                            <div>
                                <label className="block text-xs font-bold leading-6 text-black mb-2 uppercase tracking-widest">
                                    Password
                                </label>
                                <input
                                    name="password"
                                    type="password"
                                    required
                                    value={formData.password}
                                    onChange={handleChange}
                                    className="block w-full border-2 border-black py-3 px-4 text-black outline-none focus:ring-0 focus:border-[#ed7844] sm:text-sm transition-colors duration-200 bg-white"
                                />
                            </div>

                            <div>
                                <label className="block text-xs font-bold leading-6 text-black mb-2 uppercase tracking-widest">
                                    Confirm Password
                                </label>
                                <input
                                    name="confirmPassword"
                                    type="password"
                                    required
                                    value={formData.confirmPassword}
                                    onChange={handleChange}
                                    className="block w-full border-2 border-black py-3 px-4 text-black outline-none focus:ring-0 focus:border-[#ed7844] sm:text-sm transition-colors duration-200 bg-white"
                                />
                            </div>
                        </div>

                        <div className="pt-4">
                            <button
                                type="submit"
                                disabled={isLoading}
                                className="group relative flex w-full justify-center bg-[#ed7844] border-2 border-black px-3 py-4 text-sm font-black uppercase tracking-widest text-black hover:text-white hover:bg-black disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-300 ease-[cubic-bezier(0.25,1,0.5,1)] mt-2"
                            >
                                {isLoading ? 'Creating account...' : 'Sign Up'}
                            </button>
                        </div>

                        <div className="text-center text-sm pt-4 border-t-2 border-black/10">
                            <span className="text-gray-600 font-medium">Already have an account? </span>
                            <Link
                                to="/login"
                                className="font-black text-[#ed7844] hover:text-black transition-colors duration-300"
                            >
                                Log in
                            </Link>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default Register;
