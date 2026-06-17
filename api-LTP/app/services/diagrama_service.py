
import os
import uuid

import requests


class DiagramaService:

    def __init__(self):
        self.kroki_base_url = "https://kroki.io/plantuml"
        self.tipo_slug = {
            "classe": "class",
            "sequencia": "sequence",
            "atividade": "activity",
            "caso_de_uso": "usecase",
            "entidade-relacionamento": "er",
            "mindmap": "mindmap",
            "timeline": "timeline",
        }
        self.diagramas_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "assets", "diagramas"
        )
        os.makedirs(self.diagramas_dir, exist_ok=True)

    def _kroki_render(self, codigo_puml, fmt="png"):
        url = f"{self.kroki_base_url}/{fmt}"
        response = requests.post(
            url,
            headers={"Content-Type": "text/plain; charset=utf-8"},
            data=codigo_puml.encode("utf-8"),
            timeout=20,
        )
        response.raise_for_status()
        return response.content

    def gerar_diagrama(self, tipo, titulo, codigo_puml):
        if not codigo_puml or not codigo_puml.strip():
            return {
                "id": None,
                "erro": "O código PlantUML não pode ser vazio.",
            }

        slug = self.tipo_slug.get(tipo, tipo)
        titulo_slug = titulo.lower().replace(" ", "_").replace("/", "_")[:30]
        diagrama_id = uuid.uuid4().hex[:8]
        base_name = f"{diagrama_id}_{slug}_{titulo_slug}"

        puml_path = os.path.join(self.diagramas_dir, f"{base_name}.puml")
        png_path = os.path.join(self.diagramas_dir, f"{base_name}.png")

        png_bytes = self._kroki_render(codigo_puml, fmt="png")

        with open(puml_path, "w", encoding="utf-8") as f:
            f.write(codigo_puml)

        with open(png_path, "wb") as f:
            f.write(png_bytes)

        return {
            "id": diagrama_id,
            "tipo": tipo,
            "titulo": titulo,
            "png_path": png_path,
            "puml_path": puml_path,
            "png_filename": f"{base_name}.png",
            "erro": None,
        }


diagrama_service = DiagramaService()
