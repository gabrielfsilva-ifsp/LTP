
import uuid

from app.models.amizade import Amizade


class AmizadeDAO:

    amizades = [
        Amizade(
            id="amz-001",
            solicitante_id="user-A",
            alvo_id="user-B",
            status="aceita",
            criado_em="2026-05-15T09:00:00",
        ),
        Amizade(
            id="amz-002",
            solicitante_id="user-C",
            alvo_id="user-A",
            status="pendente",
            criado_em="2026-06-01T16:20:00",
        ),
    ]

    def listar_todos(self):
        return list(self.amizades)

    def buscar_por_id(self, id):
        for amizade in self.amizades:
            if amizade.id == id:
                return amizade
        return None

    def inserir(self, amizade):
        if not amizade.id:
            amizade.id = str(uuid.uuid4())
        self.amizades.append(amizade)
        return amizade

    def atualizar_status(self, id, novo_status):
        amizade = self.buscar_por_id(id)
        if not amizade:
            return None

        if novo_status == "aceita":
            if not amizade.aceitar():
                return None
        elif novo_status == "recusada":
            if not amizade.recusar():
                return None
        else:
            return None

        return amizade

    def remover(self, id):
        for i, amizade in enumerate(self.amizades):
            if amizade.id == id:
                return self.amizades.pop(i)
        return None


amizade_dao = AmizadeDAO()
