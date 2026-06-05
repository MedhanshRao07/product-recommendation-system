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
        console.log(`Login.jsx: Attempting to log in user: ${email}`);
        setIsLoading(true);
        setError('');

        try {
            const data = await authService.login(email, password);
            console.log('Login.jsx: Successful login. Redirecting to dashboard...', data);
            window.dispatchEvent(new Event('authChange'));

            setEmail('');
            setPassword('');
            navigate('/dashboard');
        } catch (err) {
            console.error('Login.jsx: Login error encountered:', err);
            if (err.response && err.response.data && err.response.data.error) {
                console.log('Login.jsx: Setting form error state to provided error message');
                setError(err.response.data.error);
            } else {
                console.log('Login.jsx: Setting generic error message');
                setError('Something went wrong during login.');
            }
        } finally {
            console.log('Login.jsx: Finished login attempt execution');
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-[#f4f4f4] py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-md w-full space-y-8 bg-white p-10 border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]">
                <div>
                    <h2 className="mt-2 text-center text-4xl font-extrabold tracking-tight text-black uppercase">
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
                            <label className="block text-sm font-bold leading-6 text-black mb-2 uppercase tracking-wide">
                                Email
                            </label>
                            <input
                                id="email"
                                type="email"
                                required
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className="block w-full border-2 border-black py-3 px-4 text-black outline-none focus:ring-0 focus:border-[#ed7844] sm:text-sm transition-colors duration-200 bg-white"
                                placeholder="..."
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-bold leading-6 text-black mb-2 uppercase tracking-wide">
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

                    <div className="pt-4">
                        <button
                            type="submit"
                            disabled={isLoading}
                            className="group relative flex w-full justify-center bg-[#ed7844] border-2 border-black px-3 py-4 text-sm font-extrabold uppercase tracking-widest text-black hover:text-white hover:bg-black disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
                        >
                            {isLoading ? 'Logging in...' : 'Log In'}
                        </button>
                    </div>

                    <div className="text-center text-sm pt-4 border-t-2 border-black/10">
                        <span className="text-gray-600 font-medium">Don't have an account? </span>
                        <Link
                            to="/register"
                            className="font-extrabold text-[#ed7844] hover:text-black transition-colors"
                        >
                            Sign up
                        </Link>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default Login;
