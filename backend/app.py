from backend import create_app
from backend.extensions import db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Only for development: creates tables if they don't exist yet
        # Ensure the mysql database 'product_rec_db' is created manually in mysql server before running
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
