-- Suggestify Database Schema v2.0
-- Updated with subcategory, popularity_score, and proper indexes

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    reset_token VARCHAR(255) DEFAULT NULL,
    reset_token_expiry DATETIME DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    brand VARCHAR(100),
    price FLOAT,
    rating FLOAT,
    image_url TEXT,
    description TEXT,
    tags VARCHAR(500),
    features TEXT,
    amazon_url TEXT,
    flipkart_url TEXT,
    myntra_url TEXT,
    price_range VARCHAR(20),
    popularity_score FLOAT DEFAULT 0.0,
    INDEX idx_category (category),
    INDEX idx_subcategory (subcategory),
    INDEX idx_brand (brand),
    INDEX idx_rating (rating),
    INDEX idx_price_range (price_range)
);

CREATE TABLE IF NOT EXISTS user_activity (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    action VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_product_id (product_id),
    INDEX idx_created_at (created_at),
    INDEX idx_user_action (user_id, action)
);

CREATE TABLE IF NOT EXISTS user_preferences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category VARCHAR(100),
    max_price FLOAT,
    min_rating FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
