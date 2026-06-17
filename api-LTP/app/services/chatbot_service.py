
import json
import logging
import os
import time
from datetime import datetime

from configuracoes import (
    build_luna_system_prompt,
    gemini_api_key,
    modelo_chatbot,
    tavily_api_key,
)
from google import genai
from google.genai import types
from tavily import TavilyClient

from app.services.diagrama_service import diagrama_service

logger = logging.getLogger(__name__)


class ChatbotService:

    def __init__(self):
        self.skills_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "skills")
        self.skills_cache = None

    def _get_available_skills(self):
        if not os.path.exists(self.skills_dir):
            return "Nenhuma skill encontrada."
        blocks = []
        loaded = []
        for folder_name in sorted(os.listdir(self.skills_dir)):
            skill_path = os.path.join(self.skills_dir, folder_name, "SKILL.md")
            if os.path.exists(skill_path):
                with open(skill_path, "r", encoding="utf-8") as f:
                    content = f.read()
                blocks.append(f"### skill: {folder_name}\n{content}")
                loaded.append(folder_name)
        if loaded:
            logger.debug("Skills carregadas: %s", ", ".join(loaded))
        return "\n\n".join(blocks) if blocks else "Nenhuma skill encontrada."

    def _load_skill(self, skill_nome, arquivo=""):
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
            return "Erro: TAVILY_API_KEY não configurada. Adicione ao .env."

        client = TavilyClient(api_key=tavily_api_key)
        response = client.search(
            query=query,
            search_depth="advanced",
            max_results=5,
            chunks_per_source=5,
        )
        results = response.get("results", [])
        if not results:
            return "Nenhum resultado encontrado para a query."

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

    def _gerar_diagrama_fn(self, tipo, titulo, codigo_puml):
        resultado = diagrama_service.gerar_diagrama(tipo, titulo, codigo_puml)
        if resultado.get("erro"):
            return f"Erro ao gerar diagrama: {resultado['erro']}"

        return json.dumps({
            "sucesso": True,
            "tipo": tipo,
            "titulo": titulo,
            "png_path": resultado["png_path"],
            "puml_path": resultado["puml_path"],
            "png_filename": resultado["png_filename"],
        }, ensure_ascii=False)


    def get_skills_string(self):
        if self.skills_cache is None:
            self.skills_cache = self._get_available_skills()
        return self.skills_cache

    def processar_mensagem(self, dados):
        prompt = dados.get("prompt", "").strip()
        if not prompt:
            return None, "O campo 'prompt' é obrigatório."
        if len(prompt) > 4000:
            return None, "O prompt não pode exceder 4000 caracteres."

        if not gemini_api_key:
            return None, "GEMINI_API_KEY não configurada. Adicione ao .env."

        tool_declarations = [
            types.Tool(function_declarations=[
                types.FunctionDeclaration(
                    name="load_skill",
                    description="Consulta conhecimento local sobre BraganTec, diagramas UML ou cartões CRC.",
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
                    description="Pesquisa na internet via Tavily (motor de busca para IA, dados em tempo real).",
                    parameters=types.Schema(
                        type="OBJECT",
                        properties={"query": types.Schema(type="STRING")},
                        required=["query"],
                    ),
                ),
                types.FunctionDeclaration(
                    name="gerar_diagrama",
                    description=(
                        "Gera diagramas de vários tipos em arquivo .puml (PlantUML) e imagem .png. "
                        "Tipos suportados: 'classe', 'sequencia', 'atividade', 'caso_de_uso', 'mindmap', 'timeline'. "
                        "SEMPRE carregue a skill 'uml-diagrams' antes."
                    ),
                    parameters=types.Schema(
                        type="OBJECT",
                        properties={
                            "tipo": types.Schema(type="STRING", description="Tipo do diagrama."),
                            "titulo": types.Schema(type="STRING", description="Título curto do diagrama."),
                            "codigo_puml": types.Schema(type="STRING", description="Código PlantUML completo."),
                        },
                        required=["tipo", "titulo", "codigo_puml"],
                    ),
                ),
            ])
        ]

        tool_dispatch = {
            "load_skill": self._load_skill,
            "search_online": self._search_online,
            "gerar_diagrama": self._gerar_diagrama_fn,
        }

        client = genai.Client(api_key=gemini_api_key)
        system_instruction = build_luna_system_prompt(skills_str=self.get_skills_string())

        pergunta_atual = [types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        )]

        chamadas_funcao_log = []
        texto_completo = ""
        historico = []

        while True:
            logger.debug("Luna (não-streaming) — enviando requisição...")
            resposta = client.models.generate_content(
                model=modelo_chatbot,
                contents=historico + pergunta_atual,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    tools=tool_declarations,
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
                        texto_completo += part.text

            historico.extend(pergunta_atual)
            historico.append(types.Content(role="model", parts=parts_modelo))

            if not function_calls:
                break

            time.sleep(3)

            partes_resposta = []
            for fc in function_calls:
                args = dict(fc.args or {})
                func = tool_dispatch.get(fc.name)
                if func:
                    resultado = func(**args)
                else:
                    resultado = f"Ferramenta '{fc.name}' não encontrada."

                chamadas_funcao_log.append({
                    "nome": fc.name,
                    "args": args,
                    "resultado": resultado,
                })

                partes_resposta.append(
                    types.Part.from_function_response(name=fc.name, response={"result": resultado})
                )

            pergunta_atual = [types.Content(role="user", parts=partes_resposta)]

        return {
            "prompt": prompt,
            "resposta": texto_completo,
            "chamadas_funcao": chamadas_funcao_log,
            "modelo": modelo_chatbot,
            "criado_em": datetime.now().isoformat(),
        }, None


chatbot_service = ChatbotService()
