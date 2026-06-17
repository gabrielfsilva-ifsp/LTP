
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from datetime import datetime


class Projeto:

    status_validos = ["rascunho", "em_andamento", "concluido", "cancelado"]

    def __init__(
        self,
        id,
        nome,
        categoria,
        resumo="",
        palavras_chave="",
        introducao="",
        objetivo_geral="",
        objetivos_especificos=None,
        metodologia="",
        cronograma=None,
        resultados_esperados="",
        referencias_bibliograficas="",
        status="rascunho",
        criado_em=None,
    ):
        self.id = id
        self.nome = nome.strip() if (nome and hasattr(nome, "strip")) else (nome or "")
        self.categoria = categoria
        self.resumo = resumo
        self.palavras_chave = palavras_chave
        self.introducao = introducao
        self.objetivo_geral = objetivo_geral
        self.objetivos_especificos = objetivos_especificos if objetivos_especificos is not None else []
        self.metodologia = metodologia
        self.cronograma = cronograma if cronograma is not None else {}
        self.resultados_esperados = resultados_esperados
        self.referencias_bibliograficas = referencias_bibliograficas
        self.status = status
        self.criado_em = criado_em or datetime.now().isoformat()

    def __str__(self):
        return (
            f"Projeto[id={self.id}, nome={self.nome!r}, "
            f"categoria={self.categoria!r}, status={self.status!r}]"
        )

    def validar_campos(self):
        obrigatorios = {
            "nome": self.nome,
            "categoria": self.categoria,
            "resumo": self.resumo,
            "objetivo_geral": self.objetivo_geral,
        }
        return [campo for campo, valor in obrigatorios.items() if not valor or not str(valor).strip()]

    def atualizar_status(self, novo_status):
        if novo_status in self.status_validos:
            self.status = novo_status
            return True
        return False

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "categoria": self.categoria,
            "resumo": self.resumo,
            "palavras_chave": self.palavras_chave,
            "introducao": self.introducao,
            "objetivo_geral": self.objetivo_geral,
            "objetivos_especificos": self.objetivos_especificos,
            "metodologia": self.metodologia,
            "cronograma": self.cronograma,
            "resultados_esperados": self.resultados_esperados,
            "referencias_bibliograficas": self.referencias_bibliograficas,
            "status": self.status,
            "criado_em": self.criado_em,
        }
