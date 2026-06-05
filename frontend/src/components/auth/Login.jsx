import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import authService from '../../services/authService';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');

        try {
            await authService.login(email, password);
            window.dispatchEvent(new Event('authChange'));
            setEmail('');
            setPassword('');
            navigate('/dashboard');
        } catch (err) {
            if (err.response && err.response.data && err.response.data.error) {
                setError(err.response.data.error);
            } else {
                setError('Something went wrong during login.');
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
                        Discover products tailored to your style.
                    </h1>
                    <p className="text-gray-400 text-lg font-medium leading-relaxed mb-10">
                        Smarter shopping powered by AI. Experience personalized recommendations curated just for you.
                    </p>
                    <div className="space-y-5">
                        <div className="flex items-center gap-4 text-gray-300 font-bold text-sm tracking-wide uppercase">
                            <span className="w-6 h-6 rounded-full bg-[#ed7844]/20 text-[#ed7844] flex items-center justify-center border border-[#ed7844]/50">✓</span> Personalized recommendations
                        </div>
                        <div className="flex items-center gap-4 text-gray-300 font-bold text-sm tracking-wide uppercase">
                            <span className="w-6 h-6 rounded-full bg-[#ed7844]/20 text-[#ed7844] flex items-center justify-center border border-[#ed7844]/50">✓</span> Smart product discovery
                        </div>
                        <div className="flex items-center gap-4 text-gray-300 font-bold text-sm tracking-wide uppercase">
                            <span className="w-6 h-6 rounded-full bg-[#ed7844]/20 text-[#ed7844] flex items-center justify-center border border-[#ed7844]/50">✓</span> Faster shopping experience
                        </div>
                    </div>
                </div>
            </div>

            {/* RIGHT SIDE: Auth Card */}
            <div className="w-full lg:w-1/2 flex items-center justify-center p-4 sm:p-6 lg:p-8 animate-fadeIn duration-500">
                <div className="max-w-md w-full space-y-8 bg-white p-10 border-2 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]">
                    <div>
                        <h2 className="mt-2 text-center text-4xl font-black tracking-tight text-black uppercase">
                            Welcome Back
                        </h2>
                        <p className="mt-3 text-center text-sm text-gray-600 font-medium">
                            Please enter your details to log in.
                        </p>
                    </div>

                    {error && (
                        <div className="bg-red-50 text-red-500 p-4 border-2 border-red-500 text-sm font-bold flex items-center justify-center">
                            {error}
                        </div>
                    )}

                    <form className="mt-8 space-y-6" onSubmit={handleLogin}>
                        <div className="space-y-6">
                            <div>
                                <label className="block text-xs font-bold leading-6 text-black mb-2 uppercase tracking-widest">
                                    Email
                                </label>
                                <input
                                    id="email"
                                    type="email"
                                    required
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    className="block w-full border-2 border-black py-3 px-4 text-black outline-none focus:ring-0 focus:border-[#ed7844] sm:text-sm transition-colors duration-200 bg-white"
                                    placeholder="your@email.com"
                                />
                            </div>
                            <div>
                                <label className="block text-xs font-bold leading-6 text-black mb-2 uppercase tracking-widest">
                                    Password
                                </label>
                                <input
                                    id="password"
                                    type="password"
                                    required
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className="block w-full border-2 border-black py-3 px-4 text-black outline-none focus:ring-0 focus:border-[#ed7844] sm:text-sm transition-colors duration-200 bg-white"
                                    placeholder="••••••••"
                                />
                            </div>
                        </div>

                        <div className="flex items-center justify-end pt-2">
                            <div className="text-sm">
                                <Link to="/forgot-password" className="font-bold text-[#ed7844] hover:text-black transition-colors duration-200">
                                    Forgot password?
                                </Link>
                            </div>
                        </div>

                        <div className="pt-2">
                            <button
                                type="submit"
                                disabled={isLoading}
                                className="group relative flex w-full justify-center bg-[#ed7844] border-2 border-black px-3 py-4 text-sm font-black uppercase tracking-widest text-black hover:text-white hover:bg-black disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-300 ease-[cubic-bezier(0.25,1,0.5,1)]"
                            >
                                {isLoading ? 'Logging in...' : 'Log In'}
                            </button>
                        </div>

                        <div className="text-center text-sm pt-4 border-t-2 border-black/10">
                            <span className="text-gray-600 font-medium">Don't have an account? </span>
                            <Link
                                to="/register"
                                className="font-black text-[#ed7844] hover:text-black transition-colors duration-300"
                            >
                                Sign up
                            </Link>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default Login;
