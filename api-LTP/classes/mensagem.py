
from datetime import datetime


class Mensagem:

    remetentes_validos = ["user", "luna"]

    def __init__(self, id, conteudo, remetente, criado_em=None):
        self.id = id
        self.conteudo = conteudo.strip() if (conteudo and hasattr(conteudo, "strip")) else (conteudo or "")
        self.remetente = remetente
        self.criado_em = criado_em or datetime.now().isoformat()

    def __str__(self):
        preview = self.conteudo[:60] + "..." if len(self.conteudo) > 60 else self.conteudo
        return f"Mensagem[id={self.id}, remetente={self.remetente!r}, conteudo={preview!r}]"

    def to_dict(self):
        return {
            "id": self.id,
            "conteudo": self.conteudo,
            "remetente": self.remetente,
            "criado_em": self.criado_em,
        }
