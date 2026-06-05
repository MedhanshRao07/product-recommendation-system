import React, { createContext, useContext, useState, useEffect } from 'react';
import authService from '../services/authService';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const checkAuth = async () => {
            try {
                const userData = await authService.getCurrentUser();
                setUser(userData);
            } catch (error) {
                // Ignore, user is not logged in or token expired
                setUser(null);
                authService.logout(); // Ensure clean state
            } finally {
                setLoading(false);
            }
        };

        checkAuth();

        const handleAuthChange = async () => {
            setLoading(true);
            await checkAuth();
        };

        window.addEventListener('authChange', handleAuthChange);
        return () => window.removeEventListener('authChange', handleAuthChange);
    }, []);

    const login = async (email, password) => {
        const response = await authService.login(email, password);
        window.dispatchEvent(new Event('authChange'));
        return response;
    };

    const register = async (name, email, password) => {
        return await authService.register(name, email, password);
    };

    const logout = () => {
        authService.logout();
        setUser(null);
    };

    if (loading) {
        // App-wide loading skeleton during initial auth check
        return (
            <div className="min-h-screen flex items-center justify-center bg-[#F4F4F5]">
                <div className="animate-pulse flex flex-col items-center">
                    <div className="h-10 w-48 bg-gray-200 mb-4 rounded-sm"></div>
                    <div className="h-4 w-32 bg-gray-200 rounded-sm"></div>
                </div>
            </div>
        );
    }

    return (
        <AuthContext.Provider value={{ user, login, register, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
};
