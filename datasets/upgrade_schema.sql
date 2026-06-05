-- Migration script to upgrade Suggestify database schema for Part 2

-- Add new columns to the products table
-- We use a series of ALTER TABLE statements. In MySQL, IF NOT EXISTS for columns isn't directly supported in older versions,
-- but we can write them directly for this development project.

ALTER TABLE products 
ADD COLUMN tags VARCHAR(500) DEFAULT NULL,
ADD COLUMN features TEXT DEFAULT NULL,
ADD COLUMN amazon_url TEXT DEFAULT NULL,
ADD COLUMN flipkart_url TEXT DEFAULT NULL,
ADD COLUMN myntra_url TEXT DEFAULT NULL,
ADD COLUMN price_range VARCHAR(20) DEFAULT NULL;
