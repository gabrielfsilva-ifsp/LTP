
import uuid

from app.models.amizade import Amizade

from app.dao.amizade_dao import amizade_dao


class AmizadeService:

    def listar_amizades(self):
        amizades = amizade_dao.listar_todos()
        return [a.to_dict() for a in amizades]

    def buscar_amizade(self, id):
        amizade = amizade_dao.buscar_por_id(id)
        if not amizade:
            return None
        return amizade.to_dict()

    def solicitar_amizade(self, dados):
        solicitante_id = dados.get("solicitante_id", "").strip()
        alvo_id = dados.get("alvo_id", "").strip()

        if not solicitante_id or not alvo_id:
            return None, "Os campos 'solicitante_id' e 'alvo_id' são obrigatórios."

        if solicitante_id == alvo_id:
            return None, "Um usuário não pode solicitar amizade a si mesmo."

        amizade = Amizade(
            id=str(uuid.uuid4()),
            solicitante_id=solicitante_id,
            alvo_id=alvo_id,
        )

        amizade_dao.inserir(amizade)
        return amizade.to_dict(), None

    def atualizar_status_amizade(self, id, dados):
        novo_status = dados.get("status", "").strip()

        if not novo_status:
            return None, "O campo 'status' é obrigatório. Use: aceita, recusada"

        if novo_status not in ["aceita", "recusada"]:
            return None, "Status inválido. Use: aceita, recusada"

        amizade = amizade_dao.atualizar_status(id, novo_status)

        if amizade is None:
            return None, "Solicitação de amizade não encontrada ou transição de status inválida."

        return amizade.to_dict(), None

    def remover_amizade(self, id):
        amizade = amizade_dao.remover(id)
        if not amizade:
            return None
        return amizade.to_dict()


amizade_service = AmizadeService()
