---
description: "Banco de dados de projetos premiados em edições anteriores da BraganTec. Use para fornecer exemplos reais, inspiração de temas e referências de escrita científica."
---

## Como Usar

### Passo 1 — Listar Anos Disponíveis
Chame `load_skill(skill_nome='projetos-vencedores')` **sem arquivo**. Isso retornará a tabela de anos disponíveis e as regras de consulta.

### Passo 2 — Carregar Conteúdo Específico
Após ver os anos disponíveis, chame `load_skill(skill_nome='projetos-vencedores', arquivo='nome_do_arquivo.md')` (ex: `arquivo='premiação2024.md'`) para ler os detalhes dos vencedores.

### Passo 3 — Filtrar e Apresentar
Filtre os projetos que mais se assemelham à área de interesse do usuário ou ao projeto dele (obtido via `obter_projetos_usuario()`). Apresente o nome do projeto, categoria e o porquê de ser uma boa referência.

## Regras

- ✅ **Duas Chamadas**: Esta skill exige 2 chamadas (Call 1: Índice → Call 2: Conteúdo).
- ✅ Destaque o que tornou o projeto vencedor (Inovação, impacto social, rigor metodológico).
- ✅ Use como benchmark: "Veja como o projeto X (vencedor em 2023) estruturou a metodologia dele".
- ❌ NUNCA invente projetos vencedores ou anos que não estão no índice.
- ❌ Não carregue todos os anos de uma vez; foque no ano mais recente ou no mais relevante para a dúvida.
- ❌ Não confunda projetos vencedores com os projetos do usuário atual.
