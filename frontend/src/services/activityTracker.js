import axios from 'axios';

const API_URL = (process.env.REACT_APP_API_URL || 'http://localhost:5000');

// Generate or retrieve session ID
const getSessionId = () => {
  let sessionId = sessionStorage.getItem('suggestify_session');
  if (!sessionId) {
    sessionId = 'sess_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    sessionStorage.setItem('suggestify_session', sessionId);
  }
  return sessionId;
};

// Get user ID from localStorage if logged in
const getUserId = () => {
  try {
    const userStr = localStorage.getItem('user');
    if (userStr) {
      const parsed = JSON.parse(userStr);
      if (parsed.user && parsed.user.id) return parsed.user.id;
    }
  } catch (e) { /* ignore */ }
  return 0; // anonymous
};

// Track user activity
const track = async (action, productId = null, metadata = {}) => {
  try {
    const userId = getUserId();
    if (productId && userId > 0) {
      await axios.post(`${API_URL}/products/track-activity`, {
        user_id: userId,
        product_id: productId,
        action: action
      });
    }
    // Also log locally for session analytics
    const log = JSON.parse(sessionStorage.getItem('activity_log') || '[]');
    log.push({
      action,
      product_id: productId,
      user_id: userId,
      session_id: getSessionId(),
      timestamp: new Date().toISOString(),
      ...metadata
    });
    // Keep last 200 entries
    if (log.length > 200) log.splice(0, log.length - 200);
    sessionStorage.setItem('activity_log', JSON.stringify(log));

    // Dispatch event so UI can dynamically refresh recommendations
    window.dispatchEvent(new CustomEvent('activityTracked', { detail: { action, productId } }));
  } catch (e) {
    // Silent fail — don't interrupt UX
  }
};

const activityTracker = {
  trackView: (productId) => track('view', productId),
  trackClick: (productId) => track('click', productId),
  trackSearch: (query) => track('search', null, { query }),
  trackCategoryVisit: (category) => track('category_visit', null, { category }),
  trackRecommendationClick: (productId) => track('recommendation_click', productId),
  trackCompareClick: (productId, site) => track('compare_click', productId, { site }),
  trackAddToCart: (productId) => track('add_to_cart', productId),
  trackPurchase: (productId) => track('purchase', productId),
  getSessionLog: () => JSON.parse(sessionStorage.getItem('activity_log') || '[]'),
  getSessionId,
  getUserId,
};

export default activityTracker;
