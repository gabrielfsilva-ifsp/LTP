
import json
import logging
import os
import re
import time
import uuid
from datetime import datetime

from app.models.projeto import Projeto
from configuracoes import (
    categorias_validas,
    gemini_api_key,
    gemini_api_key_projects_ia,
    modelo_gerador,
    tavily_api_key,
)
from google import genai
from google.genai import types
from tavily import TavilyClient

from app.dao.projeto_dao import projeto_dao

logger = logging.getLogger(__name__)


class ProjetoService:

    def __init__(self):
        self.skills_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "skills")
        self.skills_bloqueadas = {"uml-diagrams"}
        self.skills_gerador_cache = None

    def _get_skills_para_gerador(self):
        if not os.path.exists(self.skills_dir):
            return "Nenhuma skill encontrada."
        blocks = []
        loaded = []
        for folder_name in sorted(os.listdir(self.skills_dir)):
            if folder_name in self.skills_bloqueadas:
                continue
            skill_path = os.path.join(self.skills_dir, folder_name, "SKILL.md")
            if os.path.exists(skill_path):
                with open(skill_path, "r", encoding="utf-8") as f:
                    content = f.read()
                blocks.append(f"### skill: {folder_name}\n{content}")
                loaded.append(folder_name)
        if loaded:
            logger.debug("[Gerador] Skills carregadas: %s", ", ".join(loaded))
        return "\n\n".join(blocks) if blocks else "Nenhuma skill encontrada."

    def _load_skill(self, skill_nome, arquivo=""):
        if skill_nome in self.skills_bloqueadas:
            return f"Erro: A skill '{skill_nome}' não está disponível no modo gerador."

        skill_dir = os.path.join(self.skills_dir, skill_nome)
        skill_md = os.path.join(skill_dir, "SKILL.md")

        if not os.path.exists(skill_md):
            return f"Erro: Skill '{skill_nome}' não encontrada."

        if arquivo:
            filepath = os.path.join(skill_dir, arquivo)
            if not os.path.exists(filepath):
                return f"Erro: Arquivo '{arquivo}' não existe na skill '{skill_nome}'."
            with open(filepath, "r", encoding="utf-8") as f:
                return f"--- [SKILL: {skill_nome} / {arquivo}] ---\n{f.read()}"

        todos_arquivos = [f for f in os.listdir(skill_dir) if f.endswith(('.md', '.txt', '.csv'))]
        conteudo_arquivos = [f for f in todos_arquivos if f != "SKILL.md"]

        with open(skill_md, "r", encoding="utf-8") as f:
            skill_md_texto = f.read()

        if len(conteudo_arquivos) == 1:
            filepath = os.path.join(skill_dir, conteudo_arquivos[0])
            with open(filepath, "r", encoding="utf-8") as f:
                conteudo = f.read()
            return (
                f"--- [SKILL COMPLETA: {skill_nome}] ---\n"
                f"REGRAS (SKILL.md):\n{skill_md_texto}\n\n"
                f"--- CONTEÚDO: {conteudo_arquivos[0]} ---\n{conteudo}"
            )

        info = f"--- [REGRAS E ÍNDICE DA SKILL: {skill_nome}] ---\n"
        info += f"Arquivos disponíveis: {', '.join(conteudo_arquivos)}\n\n"
        info += f"REGRAS (SKILL.md):\n{skill_md_texto}"
        return info

    def _search_online(self, query):
        if not tavily_api_key:
            return "Erro: TAVILY_API_KEY não configurada."

        client = TavilyClient(api_key=tavily_api_key)
        response = client.search(
            query=query,
            search_depth="advanced",
            max_results=3,
            chunks_per_source=3,
            timeout=20,
        )
        results = response.get("results", [])
        if not results:
            return f"Nenhum resultado encontrado para '{query}'. Continue com o conhecimento que você possui."

        linhas = [f"Resultados da busca para: '{query}'\n"]
        for i, r in enumerate(results, 1):
            titulo = r.get("title", "Sem título")
            url = r.get("url", "")
            conteudo = r.get("content", "").strip()
            linhas.append(f"[{i}] {titulo}")
            linhas.append(f"    URL: {url}")
            if conteudo:
                linhas.append(f"    {conteudo}")
            linhas.append("")

        return "\n".join(linhas).strip()

    def get_skills_gerador(self):
        if self.skills_gerador_cache is None:
            self.skills_gerador_cache = self._get_skills_para_gerador()
        return self.skills_gerador_cache

    def _build_system_instruction_gerador(self):
        data_atual = datetime.now().strftime("%d/%m/%Y")
        skills_str = self.get_skills_gerador()

        prompt = f"""# PERFIL E CONTEXTO
Você é a Luna, a assistente de inteligência artificial da plataforma **IF ORBIT**.
A plataforma IF ORBIT é um ecossistema projetado para o **BRAGANTEC**, focado na feira de ciências e na gestão de projetos científicos.
Data de hoje: {data_atual}.

# SUA MISSÃO NESTE MODO (PROJECTS MODE)
Gerar um projeto científico completo seguindo RIGOROSAMENTE o esquema JSON fornecido.
Atue como uma **mentora acadêmica de elite**, garantindo nível de excelência para a BraganTec.

# REGRAS DE FORMATAÇÃO (CRÍTICAS)
1. Sua resposta final deve ser EXCLUSIVAMENTE um objeto JSON válido no mesmo modelo fornecido.
2. Use seu espaço de PENSAMENTO para planejar antes de gerar o JSON.
3. NÃO adicione textos explicativos ou saudações fora do JSON final.

# REGRAS DE CONTEÚDO
- Textos acadêmicos em português brasileiro.
- Linguagem formal mas acessível para alunos de Ensino Médio/Técnico.
- Referências bibliográficas REAIS no formato ABNT.
- Cronograma detalhado (atividades x meses de Março a Novembro).
- NUNCA gere atividades para Janeiro (1) ou Fevereiro (2).
- Objetivos específicos mensuráveis e alcançáveis.
- Use `search_online` para pesquisar tendências atuais e referências reais.
- NUNCA copie projetos existentes. 100% ORIGINAL.
- CRÍTICO (ANTI-SYCOPHANCY): Em `potencial_vitoria`, SE O TEMA FOR FRACO OU CLICHÊ, DIGA A VERDADE.

# PROTOCOLO
1. Revise as skills disponíveis e carregue as relevantes com `load_skill`.
2. Pesquise com `search_online` para embasar com dados atuais.
3. Use de 5 a 7 buscas bem direcionadas. NÃO repita buscas.
4. Gere o JSON final.

# OTIMIZAÇÃO DE COTAS (CRÍTICO)
O Gemini 3.5 Flash possui limite de 5 requisições por minuto.
Chame ferramentas em paralelo (simultaneamente) no mesmo turno sempre que possível.

# SKILLS DISPONÍVEIS:
{skills_str}

# FORMATO JSON OBRIGATÓRIO:
{{
  "nome": "Nome/título do projeto científico",
  "categoria": "Categoria do projeto (slug: ciencias_natureza_exatas | informatica | ciencias_humanas_linguagens | engenharias)",
  "resumo": "Resumo acadêmico conciso (200-280 palavras)",
  "palavras_chave": "palavra1, palavra2, palavra3, palavra4, palavra5",
  "introducao": "Introdução acadêmica (200-300 palavras)",
  "objetivo_geral": "Objetivo geral em uma frase clara",
  "objetivos_especificos": ["Objetivo 1", "Objetivo 2", "Objetivo 3"],
  "metodologia": "Metodologia detalhada (200-400 palavras)",
  "cronograma": {{
    "atividades": [
      {{"nome": "Pesquisa Bibliográfica", "meses": [3, 4]}},
      {{"nome": "Desenvolvimento do Projeto", "meses": [5, 6, 7]}},
      {{"nome": "Testes e Validação", "meses": [8, 9]}},
      {{"nome": "Finalização e Relatório", "meses": [10, 11]}}
    ]
  }},
  "resultados_esperados": "Resultados esperados (150-300 palavras)",
  "referencias_bibliograficas": "Ref 1 (ABNT)\\nRef 2 (ABNT)\\nRef 3 (ABNT)",
  "referencias_inspiracao": ["Projeto de Excelência - motivo da referência"],
  "potencial_vitoria": "Análise REALISTA do potencial na BraganTec"
}}
"""
        return prompt

    def _montar_prompt_gerador(self, tema, categoria):
        data_atual = datetime.now().strftime("%d/%m/%Y")
        prompt_tema = f'"{tema}"' if tema else "SURPREENDA-ME: Invente um tema 100% original e inovador."

        return f"""Crie um projeto científico COMPLETO sobre o seguinte tema:
{prompt_tema}
Categoria: {categoria}.
Data de hoje: {data_atual}.

Pesquise OBRIGATORIAMENTE na internet para embasar com metodologias atuais e referências reais.
Use no máximo 5 a 7 buscas bem direcionadas. Cite as URLs reais encontradas nas referências.
Retorne APENAS o JSON, sem textos explicativos fora do JSON."""

    def listar_projetos(self):
        return [p.to_dict() for p in projeto_dao.listar_todos()]

    def buscar_projeto(self, id):
        projeto = projeto_dao.buscar_por_id(id)
        if not projeto:
            return None
        return projeto.to_dict()

    def criar_projeto(self, dados):
        campos_faltando = [c for c in ["nome", "categoria"] if not dados.get(c)]
        if campos_faltando:
            return None, f"Campos obrigatórios faltando: {campos_faltando}"

        nome = dados.get("nome", "")
        if not isinstance(nome, str) or not nome.strip():
            return None, "O nome do projeto não pode ser vazio."

        categoria = dados.get("categoria", "")
        if categoria not in categorias_validas:
            return None, f"Categoria inválida: '{categoria}'. Categorias válidas: {categorias_validas}"

        status = dados.get("status", "rascunho")
        if status not in Projeto.status_validos:
            return None, f"Status inválido: '{status}'. Status válidos: {Projeto.status_validos}"

        projeto = Projeto(
            id=str(uuid.uuid4()),
            nome=nome,
            categoria=categoria,
            resumo=dados.get("resumo", ""),
            palavras_chave=dados.get("palavras_chave", ""),
            introducao=dados.get("introducao", ""),
            objetivo_geral=dados.get("objetivo_geral", ""),
            objetivos_especificos=dados.get("objetivos_especificos", []),
            metodologia=dados.get("metodologia", ""),
            cronograma=dados.get("cronograma", {}),
            resultados_esperados=dados.get("resultados_esperados", ""),
            referencias_bibliograficas=dados.get("referencias_bibliograficas", ""),
            status=status,
        )

        campos_invalidos = projeto.validar_campos()
        if campos_invalidos:
            return None, f"Campos obrigatórios não preenchidos: {campos_invalidos}"

        projeto_dao.inserir(projeto)
        return projeto.to_dict(), None

    def atualizar_projeto(self, id, dados):
        if not dados:
            return None, "Nenhum dado enviado para atualização."

        if "categoria" in dados and dados["categoria"] not in categorias_validas:
            return None, f"Categoria inválida: '{dados['categoria']}'. Categorias válidas: {categorias_validas}"

        if "status" in dados and dados["status"] not in Projeto.status_validos:
            return None, f"Status inválido: '{dados['status']}'. Status válidos: {Projeto.status_validos}"

        if "nome" in dados:
            nome = dados["nome"]
            if not isinstance(nome, str) or not nome.strip():
                return None, "O nome do projeto não pode ser vazio."

        projeto = projeto_dao.atualizar(id, dados)

        if not projeto:
            return None, None

        return projeto.to_dict(), None

    def remover_projeto(self, id):
        projeto = projeto_dao.remover(id)
        if not projeto:
            return None
        return projeto.to_dict()

    def gerar_projeto_via_ia(self, dados):
        tema = dados.get("tema", "").strip()
        categoria = dados.get("categoria", "informatica").strip()

        if not tema:
            return None, "O campo 'tema' é obrigatório para gerar o projeto."

        if categoria not in categorias_validas:
            return None, f"Categoria inválida: '{categoria}'. Use: {categorias_validas}"

        chave = gemini_api_key_projects_ia or gemini_api_key
        if not chave:
            return None, "Nenhuma chave Gemini configurada. Adicione GEMINI_API_KEY_PROJECTS_IA (ou GEMINI_API_KEY) ao .env."

        tool_declarations_gerador = [
            types.Tool(function_declarations=[
                types.FunctionDeclaration(
                    name="load_skill",
                    description="Consulta conhecimento local sobre BraganTec (regras, critérios e projetos vencedores).",
                    parameters=types.Schema(
                        type="OBJECT",
                        properties={
                            "skill_nome": types.Schema(type="STRING"),
                            "arquivo": types.Schema(type="STRING"),
                        },
                        required=["skill_nome"],
                    ),
                ),
                types.FunctionDeclaration(
                    name="search_online",
                    description="Pesquisa na internet via Tavily para buscar tendências, metodologias e referências científicas atuais.",
                    parameters=types.Schema(
                        type="OBJECT",
                        properties={"query": types.Schema(type="STRING")},
                        required=["query"],
                    ),
                ),
            ])
        ]

        tool_dispatch_gerador = {
            "load_skill": self._load_skill,
            "search_online": self._search_online,
        }

        client = genai.Client(api_key=chave)
        system_instruction = self._build_system_instruction_gerador()
        prompt_usuario = self._montar_prompt_gerador(tema, categoria)

        messages = [types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt_usuario)],
        )]

        chamadas_funcao_log = []
        texto_json = ""

        while True:
            logger.info("[Gerador] Enviando requisição — modelo=%s | tema=%s", modelo_gerador, tema[:50])

            resposta = client.models.generate_content(
                model=modelo_gerador,
                contents=messages,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    tools=tool_declarations_gerador,
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
                    thinking_config=types.ThinkingConfig(
                        thinking_level="high",
                        include_thoughts=False,
                    ),
                ),
            )

            function_calls = []
            parts_modelo = []

            if resposta.candidates and resposta.candidates[0].content:
                for part in resposta.candidates[0].content.parts:
                    parts_modelo.append(part)

                    if part.function_call:
                        function_calls.append(part.function_call)
                    elif part.text and not getattr(part, "thought", False):
                        texto_json += part.text

            messages.append(types.Content(role="model", parts=parts_modelo))

            if not function_calls:
                break

            time.sleep(3)

            partes_resposta = []
            for fc in function_calls:
                args = dict(fc.args or {})
                func = tool_dispatch_gerador.get(fc.name)
                if func:
                    resultado = func(**args)
                else:
                    resultado = f"Ferramenta '{fc.name}' não encontrada."

                chamadas_funcao_log.append({
                    "nome": fc.name,
                    "args": args,
                    "resultado": resultado[:500] if isinstance(resultado, str) else resultado,
                })

                partes_resposta.append(
                    types.Part.from_function_response(name=fc.name, response={"result": resultado})
                )

            messages.append(types.Content(role="user", parts=partes_resposta))

        if "```json" in texto_json:
            texto_json = texto_json.split("```json")[1].split("```")[0].strip()
        elif "```" in texto_json:
            texto_json = texto_json.split("```")[1].split("```")[0].strip()

        json_match = re.search(r'\{.*\}', texto_json, re.DOTALL)
        if not json_match:
            return None, "A IA não retornou um JSON válido. Tente novamente."

        projeto_json = json.loads(json_match.group(0))

        cat_gerada = projeto_json.get("categoria", categoria)
        if cat_gerada not in categorias_validas:
            cat_gerada = categoria

        projeto = Projeto(
            id=str(uuid.uuid4()),
            nome=projeto_json.get("nome", f"Projeto: {tema}"),
            categoria=cat_gerada,
            resumo=projeto_json.get("resumo", ""),
            palavras_chave=projeto_json.get("palavras_chave", ""),
            introducao=projeto_json.get("introducao", ""),
            objetivo_geral=projeto_json.get("objetivo_geral", ""),
            objetivos_especificos=projeto_json.get("objetivos_especificos", []),
            metodologia=projeto_json.get("metodologia", ""),
            cronograma=projeto_json.get("cronograma", {}),
            resultados_esperados=projeto_json.get("resultados_esperados", ""),
            referencias_bibliograficas=projeto_json.get("referencias_bibliograficas", ""),
            status="rascunho",
        )
        projeto_dao.inserir(projeto)

        return {
            "projeto": projeto.to_dict(),
            "potencial_vitoria": projeto_json.get("potencial_vitoria", ""),
            "referencias_inspiracao": projeto_json.get("referencias_inspiracao", []),
            "chamadas_funcao": chamadas_funcao_log,
            "modelo": modelo_gerador,
        }, None


projeto_service = ProjetoService()
