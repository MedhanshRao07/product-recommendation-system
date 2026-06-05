import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';

const ForgotPassword = () => {
    const [email, setEmail] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');

    const handleForgot = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');
        setMessage('');

        try {
            const res = await axios.post(
  `${process.env.REACT_APP_API_URL || 'http://localhost:5000'}/api/auth/forgot-password`,
  { email }
);
            // In a real scenario, an email is sent. For demo, we might want to log the token or show it.
            if (res.data.reset_token) {
                console.log("DEMO MODE - Reset Token:", res.data.reset_token);
                // For demo purposes, automatically navigate to reset password page with the token
                setTimeout(() => {
                    window.location.href = `/reset-password?token=${res.data.reset_token}`;
                }, 3000);
            }
        } catch (err) {
            setError(err.response?.data?.error || 'Failed to request password reset');
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
                        Lost your key?
                    </h1>
                    <p className="text-gray-400 text-lg font-medium leading-relaxed mb-10">
                        Enter your email address and we'll send you a secure link to reset your password and get you back to shopping.
                    </p>
                </div>
            </div>

            {/* RIGHT SIDE: Forgot Form */}
            <div className="w-full lg:w-1/2 flex items-center justify-center p-4 sm:p-6 lg:p-8 animate-fadeIn duration-500">
                <div className="max-w-md w-full space-y-8 bg-white p-10 border-2 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]">
                    <div>
                        <h2 className="mt-2 text-center text-4xl font-black tracking-tight text-black uppercase">
                            Reset Password
                        </h2>
                        <p className="mt-3 text-center text-sm text-gray-600 font-medium">
                            Enter the email associated with your account.
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
                            <span className="mt-2 text-xs font-normal opacity-80">(Demo mode: Redirecting to reset page...)</span>
                        </div>
                    )}

                    <form className="mt-8 space-y-6" onSubmit={handleForgot}>
                        <div>
                            <label className="block text-xs font-bold leading-6 text-black mb-2 uppercase tracking-widest">
                                Email
                            </label>
                            <input
                                type="email"
                                required
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className="block w-full border-2 border-black py-3 px-4 text-black outline-none focus:ring-0 focus:border-[#ed7844] sm:text-sm transition-colors duration-200 bg-white"
                                placeholder="your@email.com"
                            />
                        </div>

                        <div className="pt-4">
                            <button
                                type="submit"
                                disabled={isLoading || message}
                                className="group relative flex w-full justify-center bg-[#ed7844] border-2 border-black px-3 py-4 text-sm font-black uppercase tracking-widest text-black hover:text-white hover:bg-black disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-300 ease-[cubic-bezier(0.25,1,0.5,1)]"
                            >
                                {isLoading ? 'Sending...' : 'Send Reset Link'}
                            </button>
                        </div>

                        <div className="text-center text-sm pt-4 border-t-2 border-black/10">
                            <Link to="/login" className="font-black text-gray-500 hover:text-black transition-colors duration-300">
                                ← Back to Login
                            </Link>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default ForgotPassword;
