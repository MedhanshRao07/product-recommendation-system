"""
Dataset Preprocessing and Cleaning Module
=======================================
Handles the preprocessing of product data for the recommendation engine.
"""

def build_combined_text(product):
    """
    Combine product text fields into a single string for TF-IDF.

    We concatenate: name + brand + category (2x weight) + description + tags
    Missing values are replaced with empty strings to avoid errors.
    """
    name = str(product.get('name', '') or '')
    brand = str(product.get('brand', '') or '')
    category = str(product.get('category', '') or '')
    description = str(product.get('description', '') or '')
    tags = str(product.get('tags', '') or '')
    features = str(product.get('features', '') or '')

    # Repeat category and brand to give them extra weight in TF-IDF
    combined = f"{name} {brand} {brand} {category} {category} {description} {tags} {features}"
    return combined.strip()


def compute_price_range(price):
    """Classify price into a range category."""
    if price is None:
        return 'unknown'
    try:
        price = float(price)
    except (ValueError, TypeError):
        return 'unknown'
        
    if price < 50:
        return 'budget'
    elif price < 150:
        return 'mid-range'
    elif price < 500:
        return 'premium'
    else:
        return 'luxury'
