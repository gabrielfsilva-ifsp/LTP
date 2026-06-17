
from flask import Blueprint, jsonify, request

from app.services.amizade_service import amizade_service

amizade_bp = Blueprint("amizades", __name__, url_prefix="/api/amizades")


@amizade_bp.route("", methods=["GET"])
def get_amizades():
    return jsonify(amizade_service.listar_amizades()), 200


@amizade_bp.route("/<string:id>", methods=["GET"])
def get_amizade(id):
    amizade = amizade_service.buscar_amizade(id)
    if not amizade:
        return jsonify({"erro": f"Amizade '{id}' não encontrada."}), 404
    return jsonify(amizade), 200


@amizade_bp.route("", methods=["POST"])
def post_amizade():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Body JSON obrigatório."}), 400

    amizade, erro = amizade_service.solicitar_amizade(dados)
    if erro:
        return jsonify({"erro": erro}), 400

    return jsonify(amizade), 201


@amizade_bp.route("/<string:id>", methods=["PUT"])
def put_amizade(id):
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Body JSON obrigatório com campo 'status'."}), 400

    amizade, erro = amizade_service.atualizar_status_amizade(id, dados)
    if erro:
        return jsonify({"erro": erro}), 400
    if amizade is None:
        return jsonify({"erro": f"Amizade '{id}' não encontrada."}), 404

    return jsonify(amizade), 200


@amizade_bp.route("/<string:id>", methods=["DELETE"])
def delete_amizade(id):
    amizade = amizade_service.remover_amizade(id)
    if not amizade:
        return jsonify({"erro": f"Amizade '{id}' não encontrada."}), 404
    return jsonify(amizade), 200
