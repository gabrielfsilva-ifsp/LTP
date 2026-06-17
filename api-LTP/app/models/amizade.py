
from datetime import datetime


class Amizade:

    status_validos = ["pendente", "aceita", "recusada"]

    def __init__(self, id, solicitante_id, alvo_id, status="pendente", criado_em=None):
        self.id = id
        self.solicitante_id = solicitante_id
        self.alvo_id = alvo_id
        self.status = status
        self.criado_em = criado_em or datetime.now().isoformat()

    def __str__(self):
        return (
            f"Amizade[id={self.id}, de={self.solicitante_id} → {self.alvo_id}, "
            f"status={self.status!r}]"
        )

    def aceitar(self):
        if self.status == "pendente":
            self.status = "aceita"
            return True
        return False

    def recusar(self):
        if self.status == "pendente":
            self.status = "recusada"
            return True
        return False

    def to_dict(self):
        return {
            "id": self.id,
            "solicitante_id": self.solicitante_id,
            "alvo_id": self.alvo_id,
            "status": self.status,
            "criado_em": self.criado_em,
        }
