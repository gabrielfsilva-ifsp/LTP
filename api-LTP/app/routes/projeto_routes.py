
from flask import Blueprint, jsonify, request

from app.services.projeto_service import projeto_service

projeto_bp = Blueprint("projetos", __name__, url_prefix="/api/projetos")


@projeto_bp.route("", methods=["GET"])
def get_projetos():
    return jsonify(projeto_service.listar_projetos()), 200


@projeto_bp.route("/<string:id>", methods=["GET"])
def get_projeto(id):
    projeto = projeto_service.buscar_projeto(id)
    if not projeto:
        return jsonify({"erro": f"Projeto '{id}' não encontrado."}), 404
    return jsonify(projeto), 200


@projeto_bp.route("", methods=["POST"])
def post_projeto():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Body JSON obrigatório."}), 400

    projeto, erro = projeto_service.criar_projeto(dados)
    if erro:
        return jsonify({"erro": erro}), 400

    return jsonify(projeto), 201


@projeto_bp.route("/gerar", methods=["POST"])
def post_gerar_projeto():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Body JSON obrigatório com 'tema' e 'categoria'."}), 400

    resultado, erro = projeto_service.gerar_projeto_via_ia(dados)
    if erro:
        return jsonify({"erro": erro}), 400

    return jsonify(resultado), 201


@projeto_bp.route("/<string:id>", methods=["PUT"])
def put_projeto(id):
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Body JSON obrigatório."}), 400

    projeto, erro = projeto_service.atualizar_projeto(id, dados)
    if erro:
        return jsonify({"erro": erro}), 400
    if projeto is None:
        return jsonify({"erro": f"Projeto '{id}' não encontrado."}), 404

    return jsonify(projeto), 200


@projeto_bp.route("/<string:id>", methods=["DELETE"])
def delete_projeto(id):
    projeto = projeto_service.remover_projeto(id)
    if not projeto:
        return jsonify({"erro": f"Projeto '{id}' não encontrado."}), 404
    return jsonify(projeto), 200
