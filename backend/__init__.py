from flask import Flask
from .config import Config
from .extensions import db, bcrypt, jwt, cors

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/*": {"origins": "*"}})

    # Register blueprints here
    from .routes.auth_routes import auth_bp
    from .routes.product_routes import product_bp
    from .routes.chatbot_routes import chat_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(product_bp, url_prefix='/api/products')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')

    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Not found"}, 404

    @app.errorhandler(500)
    def internal_error(error):
        return {"error": "Internal server error"}, 500

    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}, 200

    @app.route('/trending', methods=['GET'])
    def trending_products():
        from .services.product_service import ProductService
        from flask import jsonify
        products = ProductService.get_trending_products()
        return jsonify(products), 200

    @app.route('/product/<int:product_id>', methods=['GET'])
    def get_product(product_id):
        from .services.product_service import ProductService
        from flask import jsonify
        product = ProductService.get_product_by_id(product_id)
        if product:
            return jsonify(product), 200
        return jsonify({"error": "Product not found"}), 404

    return app
