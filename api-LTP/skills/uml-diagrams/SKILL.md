---
description: "Geração de diagramas UML via PlantUML (Classe, Sequência, Atividade, Casos de Uso). Use quando o usuário pedir qualquer diagrama UML, arquitetura de sistema ou modelagem de software."
---

## Como Usar

### Passo 1 — Obter contexto do projeto
Antes de modelar, você precisa entender o que está sendo construído:
- **O usuário já forneceu detalhes?** → use-os.
- **Nenhum detalhe?** → chame  a função`obter_projetos_usuario`:
  - **1 projeto** → use-o automaticamente.
  - **Mais de 1 projeto** → **PERGUNTE** qual usar.
  - **Nenhum projeto** → peça descrição manual.

### Passo 2 — Carregar o guia de sintaxe
Chame `load_skill(skill_nome='uml-diagrams')` para acessar `uml_diagrams_guide.md`. Ele contém os `skinparam` obrigatórios para um visual profissional, configurações de estilo moderno e exemplos de sintaxe.

### Passo 3 — Gerar o diagrama
Chame a ferramenta `gerar_diagrama(tipo, titulo, codigo_puml)`:
- **Tipos aceitos**: 'classe', 'sequencia', 'atividade', 'caso_de_uso', 'er', 'mindmap', 'timeline'.
- **Título**: Curto e descritivo.
- **Código**: Use a sintaxe PlantUML fiel ao guia, incluindo sempre o bloco de estilo padrão.

### Passo 4 — Entrega
Apresente o **Preview** da imagem usando markdown `![Diagrama](url_do_png)` para que o usuário veja o diagrama imediatamente.

Abaixo da imagem, forneça os links para download usando EXATAMENTE o formato Markdown abaixo. **NÃO USE HTML.** O sistema irá estilizá-los como botões automaticamente:

[🖼️ Ver Imagem Original](URL_PNG)
[📥 Baixar .PUML](URL_PUML)

## Regras

- ✅ SEMPRE carregue `uml_diagrams_guide.md` antes de gerar para garantir a sintaxe.
- ✅ Use `skinparam` em todos os diagramas conforme o guia.
- ✅ SEMPRE inclua o **preview da imagem** e os **links markdown** de download na sua resposta final.
- ✅ **Para Diagramas de Sequência e de Classes:** OBRIGATORIAMENTE mapeie e inclua todas as camadas da arquitetura do projeto (UI/View/Telas, Controllers/Services, Models/Banco de Dados). Nunca limite o diagrama apenas ao core/domínio ou banco de dados; mostre a interação completa (ex: Usuário -> Tela -> Controller -> API -> Banco).
- ✅ NUNCA apenas descreva um diagrama em texto — SEMPRE gere o arquivo.
- ✅ Sugira o próximo diagrama natural (ex: Classe → Sequência).
- ❌ **PROIBIDO `package { }` em Diagramas de Sequência**: Pacotes (`package`) não existem no padrão de sequência PlantUML e confundem o usuário visualmente. Use apenas `actor`, `participant`, `boundary`, `control` e `entity` como participantes. Nunca agrupe participantes em pacotes, POREM, o uso de package em diagramas de classes é permitido, somente de sequencias nao tem.
- ❌ Não invente sintaxe PlantUML; use apenas o que está no guia.
- ❌ Se o usuário pedir algo ambíguo, peça esclarecimento antes de gerar.
