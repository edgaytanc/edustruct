from flask import Flask, jsonify
from flask_cors import CORS

from app.config import Config
from app.routes import all_blueprints


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(
        app,
        resources={r"/api/*": {"origins": app.config["FRONTEND_URL"]}},
        supports_credentials=True
    )

    for blueprint in all_blueprints:
        app.register_blueprint(blueprint)

    @app.route("/", methods=["GET"])
    def index():
        return jsonify(
            {
                "success": True,
                "message": f"{app.config['APP_NAME']} activa"
            }
        ), 200

    return app