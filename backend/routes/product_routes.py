from flask import Blueprint, jsonify, request
from ..services.product_service import ProductService

product_bp = Blueprint('products', __name__)

@product_bp.route('', methods=['GET'])
def get_products():
    page = request.args.get('page', type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    if page is not None:
        result = ProductService.get_all_products(page=page, per_page=per_page)
        return jsonify(result), 200
    else:
        products = ProductService.get_all_products()
        return jsonify(products), 200

@product_bp.route('/trending', methods=['GET'])
def get_trending():
    products = ProductService.get_trending_products()
    return jsonify(products), 200

@product_bp.route('/search', methods=['GET'])
def search_products():
    query = request.args.get('q', '')
    if not query.strip():
        return jsonify([]), 200
    products = ProductService.search_products(query)
    return jsonify(products), 200

@product_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = ProductService.get_categories()
    return jsonify(categories), 200

@product_bp.route('/category/<category>', methods=['GET'])
def get_products_by_category(category):
    products = ProductService.get_products_by_category(category)
    return jsonify(products), 200

@product_bp.route('/recommend', methods=['POST'])
def recommend_products():
    data = request.get_json()
    category = data.get('category')
    max_price = data.get('max_price')
    rating = data.get('rating')
    
    recommendations = ProductService.get_recommendations(category, max_price, rating)
    return jsonify({"recommendations": recommendations}), 200

@product_bp.route('/track-activity', methods=['POST'])
def track_activity():
    data = request.get_json()
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    action = data.get('action')
    
    success = ProductService.track_activity(user_id, product_id, action)
    if success:
        return jsonify({"message": "Activity tracked successfully"}), 200
    return jsonify({"error": "Failed to track activity"}), 500

@product_bp.route('/auto-recommend/<int:user_id>', methods=['GET'])
def auto_recommend(user_id):
    recommendations = ProductService.get_auto_recommendations(user_id)
    return jsonify({"recommendations": recommendations}), 200

@product_bp.route('/grouped', methods=['GET'])
def get_grouped_products():
    per_category = request.args.get('per_category', 6, type=int)
    grouped = ProductService.get_grouped_products(per_category=per_category)
    return jsonify(grouped), 200

@product_bp.route('/related/<int:product_id>', methods=['GET'])
def get_related_products(product_id):
    products = ProductService.get_related_products(product_id)
    return jsonify(products), 200
