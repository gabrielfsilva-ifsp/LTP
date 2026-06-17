

---

## Projetos (`/api/projetos`)

| Verbo HTTP | Descrição / Path | Path (Exemplo) | Body de Envio (JSON) | Body de Resposta (JSON) |
| :--- | :--- | :--- | :--- | :--- |
| **GET** | `/api/projetos` <br> Lista todos os projetos. | `GET /api/projetos` | | `[ { "id": "proj-001", "nome": "Sistema de Monitoramento...", "categoria": "meio_ambiente", "status": "em_andamento", ... } ]` |
| **GET** | `/api/projetos/{id}` <br> Busca projeto por ID. | `GET /api/projetos/proj-001` | | `{ "id": "proj-001", "nome": "Sistema de Monitoramento...", "categoria": "meio_ambiente", ... }` |
| **POST** | `/api/projetos` <br> Cria projeto manualmente. | `POST /api/projetos` | `{ "nome": "Meu Projeto", "categoria": "tecnologia", "resumo": "...", "objetivo_geral": "..." }` | `{ "id": "uuid-gerado", "nome": "Meu Projeto", "status": "rascunho", ... }` |
| **POST** | `/api/projetos/gerar` <br> Gera projeto completo via IA a partir de um tema. | `POST /api/projetos/gerar` | `{ "tema": "Energias renováveis no semiárido", "categoria": "meio_ambiente" }` | `{ "id": "uuid-gerado", "nome": "Projeto: Energias renováveis...", "resumo": "...", "objetivo_geral": "...", ... }` |
| **PUT** | `/api/projetos/{id}` <br> Atualiza campos de um projeto existente. | `PUT /api/projetos/proj-001` | `{ "status": "concluido", "resultados_esperados": "Novo texto..." }` | `{ "id": "proj-001", "status": "concluido", ... }` |
| **DELETE** | `/api/projetos/{id}` <br> Remove projeto pelo ID. Retorna o objeto removido. | `DELETE /api/projetos/proj-001` | | `{ "id": "proj-001", "nome": "Sistema de Monitoramento...", ... }` |

### Categorias válidas
`tecnologia` · `saude` · `meio_ambiente` · `educacao` · `engenharia` · `ciencias_sociais` · `outros`

### Status válidos
`rascunho` · `em_andamento` · `concluido` · `cancelado`

---

## Amizades (`/api/amizades`)

| Verbo HTTP | Descrição / Path | Path (Exemplo) | Body de Envio (JSON) | Body de Resposta (JSON) |
| :--- | :--- | :--- | :--- | :--- |
| **GET** | `/api/amizades` <br> Lista todas as amizades. | `GET /api/amizades` | | `[ { "id": "amz-001", "solicitante_id": "user-A", "alvo_id": "user-B", "status": "aceita", ... } ]` |
| **GET** | `/api/amizades/{id}` <br> Busca amizade por ID. | `GET /api/amizades/amz-001` | | `{ "id": "amz-001", "solicitante_id": "user-A", "alvo_id": "user-B", "status": "aceita", ... }` |
| **POST** | `/api/amizades` <br> Solicita amizade entre dois usuários. | `POST /api/amizades` | `{ "solicitante_id": "user-X", "alvo_id": "user-Y" }` | `{ "id": "uuid-gerado", "solicitante_id": "user-X", "alvo_id": "user-Y", "status": "pendente", ... }` |
| **PUT** | `/api/amizades/{id}` <br> Aceita ou recusa uma solicitação pendente. | `PUT /api/amizades/amz-002` | `{ "status": "aceita" }` | `{ "id": "amz-002", "status": "aceita", ... }` |
| **DELETE** | `/api/amizades/{id}` <br> Remove amizade pelo ID. Retorna o objeto removido. | `DELETE /api/amizades/amz-001` | | `{ "id": "amz-001", "solicitante_id": "user-A", ... }` |

### Status válidos para PUT
`aceita` · `recusada`

---

## Chatbot Luna (`/api/chatbot`)

| Verbo HTTP | Descrição / Path | Path (Exemplo) | Body de Envio (JSON) | Body de Resposta (JSON) |
| :--- | :--- | :--- | :--- | :--- |
| **POST** | `/api/chatbot/conversar` <br> Envia um prompt e recebe a resposta da Luna (IA). Se `GEMINI_API_KEY` estiver configurada, usa Gemini; senão, resposta simulada. | `POST /api/chatbot/conversar` | `{ "prompt": "Como criar um projeto de pesquisa?" }` | `{ "id": "uuid", "prompt": "Como criar...", "resposta": "Para criar um projeto...", "modo": "gemini", "criado_em": "2026-06-10T..." }` |

---

## Exportação PDF (`/api/pdf`)

| Verbo HTTP | Descrição / Path | Path (Exemplo) | Body de Envio (JSON) | Body de Resposta |
| :--- | :--- | :--- | :--- | :--- |
| **POST** | `/api/pdf/exportar` <br> Recebe JSON do projeto e retorna o arquivo PDF como download. | `POST /api/pdf/exportar` | `{ "nome": "Meu Projeto", "categoria": "tecnologia", "resumo": "...", "objetivo_geral": "...", "metodologia": "..." }` | Arquivo `Meu_Projeto.pdf` (download direto, `Content-Type: application/pdf`) |

---

## Respostas de Erro Padrão

| Código | Situação | Exemplo de Body |
| :--- | :--- | :--- |
| `400` | Body inválido ou campo obrigatório faltando | `{ "erro": "Campos obrigatórios faltando: ['nome']" }` |
| `404` | Recurso não encontrado | `{ "erro": "Projeto 'proj-999' não encontrado." }` |
| `405` | Método HTTP não permitido | `{ "erro": "Método HTTP não permitido.", "status": 405 }` |
