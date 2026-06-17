
import io

from app.services.pdf_service import pdf_service
from flask import Blueprint, jsonify, request, send_file

pdf_bp = Blueprint("pdf", __name__, url_prefix="/api/pdf")


@pdf_bp.route("/exportar", methods=["POST"])
def post_exportar():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Body JSON obrigatório com os dados do projeto."}), 400

    pdf_bytes, erro = pdf_service.gerar_pdf_projeto(dados)
    if erro:
        return jsonify({"erro": erro}), 400

    nome_arquivo = dados.get("nome", "projeto").replace(" ", "_")[:50] + ".pdf"

    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=nome_arquivo,
    )
