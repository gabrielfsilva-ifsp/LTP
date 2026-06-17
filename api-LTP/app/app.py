
from app.routes.amizade_routes import amizade_bp
from app.routes.chatbot_routes import chatbot_bp
from app.routes.pdf_routes import pdf_bp
from app.routes.projeto_routes import projeto_bp
from flask import Flask, jsonify


def criar_app():
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False

    app.register_blueprint(projeto_bp)
    app.register_blueprint(amizade_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(pdf_bp)

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"erro": "Rota não encontrada.", "status": 404}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"erro": "Método HTTP não permitido.", "status": 405}), 405

    return app
