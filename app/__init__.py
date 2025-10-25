from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = True

    # Importér og registrér dine ruter
    from app.views import main_bp
    app.register_blueprint(main_bp)

    return app
