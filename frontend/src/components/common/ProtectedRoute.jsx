import React from 'react';
import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ children }) => {
    // Check if unexpired JWT exists in localStorage
    const userStr = localStorage.getItem('user');

    if (!userStr) {
        // No user -> redirect to Login
        return <Navigate to="/login" replace />;
    }

    try {
        const user = JSON.parse(userStr);
        if (!user || !user.access_token) {
            return <Navigate to="/login" replace />;
        }
        // E.g. later you could check token expiration here
    } catch (err) {
        return <Navigate to="/login" replace />;
    }

    // User is authenticated
    return children;
};

export default ProtectedRoute;
