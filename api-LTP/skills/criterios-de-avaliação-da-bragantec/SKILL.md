---
description: "Critérios oficiais de avaliação e pontuação da BraganTec: eixos de nota, pesos, e o que os avaliadores observam. Use para orientar alunos sobre como melhorar seus projetos."
---

## Como Usar

### Passo 1 — Entender o contexto
O usuário quer saber como será avaliado ou quer uma "pré-avaliação" do projeto dele?

### Passo 2 — Consultar Critérios
Chame `load_skill(skill_nome='criterios-de-avaliação-da-bragantec')` para obter a tabela de pesos e eixos (ex: Inovação, Metodologia, Postura, Caderno de Bordo).

### Passo 3 — Cruzar com o Projeto
Se o usuário tiver um projeto cadastrado, use `obter_projetos_usuario()` e compare os dados (resumo/metodologia) com os critérios oficiais. 
- **Exemplo**: Se o critério "Metodologia" exige clareza e o projeto do aluno está vago, sugira melhorias específicas baseadas no documento.

### Passo 4 — Orientação Consultiva
Não apenas liste os pontos; explique **o que** o avaliador espera ver em cada categoria para que o aluno alcance a nota máxima.

## Regras

- ✅ Seja fiel aos pesos e pontuações: não arredonde ou invente valores.
- ✅ Use tabelas para mostrar a distribuição de pontos se o usuário pedir um resumo.
- ✅ Diferencie claramente o que é avaliado no **Estande** vs **Relatório/Resumo**.
- ❌ Nunca garanta nota ("Com isso você tira 10"). Use termos como "Isso ajuda a atender ao critério X".
- ❌ Não invente critérios; se o documento não cita "Design do Logotipo", não diga que isso conta pontos.
