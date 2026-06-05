// src/utils/auth.js

/**
 * Checks if a JWT string exists in localStorage.
 * Depending on your application, you might also decode the JWT to check if it's expired.
 * For now, this meets the requirement of verifying presence.
 * 
 * @returns {boolean} True if the user is considered authenticated
 */
export const isAuthenticated = () => {
    const userStr = localStorage.getItem('user');
    if (!userStr) return false;

    try {
        const user = JSON.parse(userStr);
        return !!user.access_token;
    } catch (e) {
        return false;
    }
};

/**
 * Convenience method to extract just the token if needed for API calls
 */
export const getToken = () => {
    const userStr = localStorage.getItem('user');
    if (!userStr) return null;

    try {
        const user = JSON.parse(userStr);
        return user.access_token || null;
    } catch (e) {
        return null;
    }
};
