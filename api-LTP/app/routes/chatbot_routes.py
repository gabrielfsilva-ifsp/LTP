
from app.services.chatbot_service import chatbot_service
from flask import Blueprint, jsonify, request

chatbot_bp = Blueprint("chatbot", __name__, url_prefix="/api/chatbot")


@chatbot_bp.route("/conversar", methods=["POST"])
def post_conversar():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Body JSON obrigatório com campo 'prompt'."}), 400

    resultado, erro = chatbot_service.processar_mensagem(dados)
    if erro:
        return jsonify({"erro": erro}), 400

    return jsonify(resultado), 200
