
import uuid

from app.models.projeto import Projeto


class ProjetoDAO:

    projetos = [
        Projeto(
            id="proj-001",
            nome="Sistema de Monitoramento de Queimadas com IA",
            categoria="ciencias_natureza_exatas",
            resumo="Plataforma para detecção precoce de incêndios florestais usando imagens de satélite e redes neurais convolucionais.",
            palavras_chave="satélite, IA, queimadas, Cerrado, CNN",
            introducao="O Brasil enfrenta crises recorrentes de queimadas no Cerrado...",
            objetivo_geral="Reduzir o tempo de resposta a queimadas no Cerrado em 40% usando monitoramento via satélite.",
            objetivos_especificos=[
                "Coletar imagens de satélite em tempo real via NASA FIRMS",
                "Treinar modelo CNN para detecção de focos de calor",
                "Emitir alertas automáticos para brigadas locais",
            ],
            metodologia="Uso de APIs de satélite (NASA FIRMS) + modelo CNN treinado com TensorFlow.",
            cronograma={"atividades": [
                {"nome": "Pesquisa Bibliográfica", "meses": [3, 4]},
                {"nome": "Coleta de dados", "meses": [5, 6]},
                {"nome": "Treinamento do modelo", "meses": [7, 8]},
                {"nome": "Validação e relatório", "meses": [9, 10, 11]},
            ]},
            resultados_esperados="Dashboard com mapa de calor e sistema de alertas via SMS.",
            referencias_bibliograficas="NASA FIRMS. Fire Information for Resource Management System. Disponível em: https://firms.modaps.eosdis.nasa.gov",
            status="em_andamento",
            criado_em="2026-05-10T10:00:00",
        ),
        Projeto(
            id="proj-002",
            nome="App de Saúde Mental para Estudantes do IFSP",
            categoria="informatica",
            resumo="Aplicativo mobile com recursos de mindfulness e triagem de ansiedade (GAD-7) para universitários do IFSP.",
            palavras_chave="saúde mental, ansiedade, mindfulness, universitários, GAD-7",
            introducao="Estudantes universitários apresentam altas taxas de ansiedade...",
            objetivo_geral="Disponibilizar ferramenta digital acessível de suporte à saúde mental para estudantes.",
            objetivos_especificos=[
                "Implementar questionário de triagem GAD-7",
                "Desenvolver sessões guiadas de meditação",
                "Criar dashboard de acompanhamento emocional",
            ],
            metodologia="Desenvolvimento mobile com React Native, backend Flask, banco SQLite.",
            cronograma={"atividades": [
                {"nome": "Levantamento de requisitos", "meses": [3, 4]},
                {"nome": "Desenvolvimento do app", "meses": [5, 6, 7]},
                {"nome": "Testes com usuários", "meses": [8, 9]},
                {"nome": "Finalização", "meses": [10, 11]},
            ]},
            resultados_esperados="App publicado na Play Store com 100 usuários no piloto.",
            referencias_bibliograficas="SPITZER, R. L. et al. A Brief Measure for Assessing Generalized Anxiety Disorder. Archives of Internal Medicine, 2006.",
            status="rascunho",
            criado_em="2026-05-20T14:30:00",
        ),
    ]

    def listar_todos(self):
        return list(self.projetos)

    def buscar_por_id(self, id):
        for projeto in self.projetos:
            if projeto.id == id:
                return projeto
        return None

    def inserir(self, projeto):
        if not projeto.id:
            projeto.id = str(uuid.uuid4())
        self.projetos.append(projeto)
        return projeto

    def atualizar(self, id, dados):
        projeto = self.buscar_por_id(id)
        if not projeto:
            return None

        campos_editaveis = [
            "nome", "categoria", "resumo", "palavras_chave",
            "introducao", "objetivo_geral", "objetivos_especificos",
            "metodologia", "cronograma", "resultados_esperados",
            "referencias_bibliograficas", "status",
        ]

        for campo in campos_editaveis:
            if campo in dados:
                setattr(projeto, campo, dados[campo])

        return projeto

    def remover(self, id):
        for i, projeto in enumerate(self.projetos):
            if projeto.id == id:
                return self.projetos.pop(i)
        return None


projeto_dao = ProjetoDAO()
