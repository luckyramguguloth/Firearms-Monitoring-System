from app import create_app, db
from app.models import user  # Import to register the model
from flask import Flask
from app.routes.detect import detect_bp
from app.auth.admin_routes import admin_bp



app = create_app()

# Register blueprint for detection
app.register_blueprint(detect_bp, url_prefix='/detect')

app.register_blueprint(admin_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This ensures tables are created
    app.run(debug=True)
