import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import axios from 'axios';

const ResetPassword = () => {
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');
    
    const navigate = useNavigate();
    const location = useLocation();
    
    // Extract token from URL
    const queryParams = new URLSearchParams(location.search);
    const token = queryParams.get('token');

    useEffect(() => {
        if (!token) {
            setError('Invalid or missing reset token.');
        }
    }, [token]);

    const handleReset = async (e) => {
        e.preventDefault();
        
        if (password !== confirmPassword) {
            setError('Passwords do not match');
            return;
        }
        
        if (password.length < 6) {
            setError('Password must be at least 6 characters');
            return;
        }
        
        setIsLoading(true);
        setError('');
        setMessage('');

        try {
            const res = await axios.post('http://localhost:5000/api/auth/reset-password', { 
                token, 
                password 
            });
            setMessage(res.data.message);
            setTimeout(() => {
                navigate('/login');
            }, 2500);
        } catch (err) {
            setError(err.response?.data?.error || 'Failed to reset password');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex bg-[#f4f4f4]">
            {/* LEFT SIDE: Premium Branding */}
            <div className="hidden lg:flex lg:w-1/2 bg-[#0A0A0A] p-12 flex-col justify-between relative overflow-hidden border-r-2 border-black">
                <div className="absolute inset-0 opacity-[0.03]" style={{ backgroundImage: 'linear-gradient(#fff 1px, transparent 1px), linear-gradient(90deg, #fff 1px, transparent 1px)', backgroundSize: '40px 40px' }}></div>
                <div className="relative z-10">
                    <Link to="/dashboard" className="font-black text-3xl tracking-tighter text-white uppercase hover:opacity-80 transition-opacity">
                        SUGGESTIFY<span className="text-[#ed7844]">.</span>
                    </Link>
                </div>
                <div className="relative z-10 max-w-lg mb-20">
                    <h1 className="text-5xl font-black text-white uppercase tracking-tight leading-[1.1] mb-6">
                        Secure your account.
                    </h1>
                    <p className="text-gray-400 text-lg font-medium leading-relaxed mb-10">
                        Create a strong, new password. We recommend using a mix of letters, numbers, and symbols.
                    </p>
                </div>
            </div>

            {/* RIGHT SIDE: Reset Form */}
            <div className="w-full lg:w-1/2 flex items-center justify-center p-4 sm:p-6 lg:p-8 animate-fadeIn duration-500">
                <div className="max-w-md w-full space-y-8 bg-white p-10 border-2 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]">
                    <div>
                        <h2 className="mt-2 text-center text-4xl font-black tracking-tight text-black uppercase">
                            New Password
                        </h2>
                        <p className="mt-3 text-center text-sm text-gray-600 font-medium">
                            Please enter your new password below.
                        </p>
                    </div>

                    {error && (
                        <div className="bg-red-50 text-red-500 p-4 border-2 border-red-500 text-sm font-bold flex items-center justify-center text-center">
                            {error}
                        </div>
                    )}
                    {message && (
                        <div className="bg-emerald-50 text-emerald-600 p-4 border-2 border-emerald-500 text-sm font-bold flex flex-col items-center justify-center text-center">
                            {message}
                            <span className="mt-2 text-xs font-normal opacity-80">(Redirecting to login...)</span>
                        </div>
                    )}

                    <form className="mt-8 space-y-6" onSubmit={handleReset}>
                        <div className="space-y-4">
                            <div>
                                <label className="block text-xs font-bold leading-6 text-black mb-2 uppercase tracking-widest">
                                    New Password
                                </label>
                                <input
                                    type="password"
                                    required
                                    disabled={!token}
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className="block w-full border-2 border-black py-3 px-4 text-black outline-none focus:ring-0 focus:border-[#ed7844] sm:text-sm transition-colors duration-200 bg-white disabled:bg-gray-100"
                                    placeholder="••••••••"
                                />
                            </div>
                            <div>
                                <label className="block text-xs font-bold leading-6 text-black mb-2 uppercase tracking-widest">
                                    Confirm Password
                                </label>
                                <input
                                    type="password"
                                    required
                                    disabled={!token}
                                    value={confirmPassword}
                                    onChange={(e) => setConfirmPassword(e.target.value)}
                                    className="block w-full border-2 border-black py-3 px-4 text-black outline-none focus:ring-0 focus:border-[#ed7844] sm:text-sm transition-colors duration-200 bg-white disabled:bg-gray-100"
                                    placeholder="••••••••"
                                />
                            </div>
                        </div>

                        <div className="pt-4">
                            <button
                                type="submit"
                                disabled={isLoading || message || !token}
                                className="group relative flex w-full justify-center bg-[#ed7844] border-2 border-black px-3 py-4 text-sm font-black uppercase tracking-widest text-black hover:text-white hover:bg-black disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-300 ease-[cubic-bezier(0.25,1,0.5,1)]"
                            >
                                {isLoading ? 'Resetting...' : 'Reset Password'}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default ResetPassword;
