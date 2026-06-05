import axios from 'axios';
import { getToken } from '../utils/auth';

// Ideally this comes from an environment variable (e.g. process.env.REACT_APP_API_URL)
const API_URL = 'http://localhost:5000/api/auth';

const login = async (email, password) => {
    console.log(`authService.js: Initiating login POST request to ${API_URL}/login for user ${email}`);
    const response = await axios.post(`${API_URL}/login`, {
        email,
        password,
    });
    console.log('authService.js: Login response received:', response.data);
    if (response.data.access_token) {
        localStorage.setItem('user', JSON.stringify(response.data));
    }
    return response.data;
};

const register = async (name, email, password) => {
    const response = await axios.post(`${API_URL}/register`, {
        name,
        email,
        password,
    });
    return response.data;
};

const logout = () => {
    const hasUser = localStorage.getItem('user');
    if (hasUser) {
        localStorage.removeItem('user');
        window.dispatchEvent(new Event('authChange'));
    }
};

const getCurrentUser = async () => {
    const userStr = localStorage.getItem('user');
    if (!userStr) throw new Error("No token found");

    let token = null;
    let localUser = null;
    try {
        const parsed = JSON.parse(userStr);
        token = parsed.access_token;
        localUser = parsed.user;
    } catch (e) {
        throw new Error("Invalid token format");
    }

    if (!token) throw new Error("No token found");

    try {
        const response = await axios.get(`${API_URL}/me`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });
        
        // Keep localStorage updated with fresh user data
        const newLocalUser = { access_token: token, user: response.data };
        localStorage.setItem('user', JSON.stringify(newLocalUser));
        
        return response.data;
    } catch (error) {
        console.error("Auth fetch error:", error?.response?.status);
        if (error.response && error.response.status === 401) {
            logout();
            throw error;
        }
        
        // Network error (backend offline) or other server error -> persist local state
        if (localUser) {
            console.warn("Backend unreachable, returning cached user from localStorage");
            return localUser;
        }
        throw error;
    }
};

const authService = {
    login,
    register,
    logout,
    getCurrentUser,
};

export default authService;
