from flask import Flask
from app.extensions import db, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.DevelopmentConfig')
    db.init_app(app)
    migrate.init_app(app, db)
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app