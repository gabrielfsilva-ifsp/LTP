# UML Diagrams — Guia de Geração PlantUML

## Tipos Suportados

| Tipo | Parâmetro `tipo` | Quando usar |
|------|-----------------|-------------|
| Diagrama de Classe | `classe` | Estrutura OOP, herança, atributos, métodos |
| Diagrama de Sequência | `sequencia` | Interações entre objetos ao longo do tempo |
| Diagrama de Atividade | `atividade` | Fluxos de processo, decisões, paralelismo |
| Diagrama de Casos de Uso | `caso_de_uso` | Atores, funcionalidades, relacionamentos |
| Diagrama ER (Banco de Dados) | `er` | Modelagem de dados, tabelas, PK/FK, cardinalidade |
| Mapa Mental | `mindmap` | Organização de ideias, brainstorming, hierarquias |
| Timeline (Linha do Tempo) | `timeline` | Eventos cronológicos, fases de projeto |

---

## Diagrama de Classe

### ⚠️ REGRA CRÍTICA OBRIGATÓRIA: Divisão em Camadas (Packages)

Quando o diagrama envolver classes de diferentes camadas da aplicação (ex: Controllers, Services, DAOs, Models), você **DEVE OBRIGATORIAMENTE** agrupar as classes em pacotes (`package`) correspondentes a essas pastas/camadas. **Nunca** desenhe classes de camadas distintas misturadas sem a devida divisão em packages.

#### Exemplo de Estrutura em Camadas:

```plantuml
@startuml
skinparam classBackgroundColor #1A1A2E
skinparam classBorderColor #39FF14
skinparam classHeaderBackgroundColor #0D0D1A
skinparam classFontColor #FFFFFF
skinparam packageBackgroundColor #0D0D1A
skinparam packageBorderColor #39FF14
skinparam packageFontColor #39FF14
skinparam arrowColor #39FF14
skinparam linetype ortho
skinparam nodesep 60
skinparam ranksep 60

package "Controllers" {
  class ProjetoController {
    + criar(): Response
    + listar(): Response
    + editar(id): Response
  }
}

package "Services" {
  class ProjetoService {
    - _dao: ProjetoDAO
    + criar_projeto(dados): Projeto
    + listar_por_usuario(id): List
  }
}

package "DAO" {
  class ProjetoDAO {
    - _tabela: str
    + inserir(dados): dict
    + buscar_por_id(id): Projeto
    + listar_por_lider(id): List
  }
}

package "Models" {
  class Projeto {
    + id: UUID
    + nome: str
    + status: str
    + from_dict(d): Projeto
    + to_dict(): dict
  }
}

ProjetoController --> ProjetoService : usa
ProjetoService --> ProjetoDAO : usa
ProjetoDAO --> Projeto : retorna
@enduml
```

**Prefixos de visibilidade:** `-` privado, `+` público, `#` protegido

**Relações:**
- `-->` associação simples
- `*--` composição (tem-um forte)
- `o--` agregação (tem-um fraco)
- `<|--` herança (é-um)

**Quando usar packages:**
- ✅ SEMPRE que houver múltiplas camadas (Controller/Service/DAO/Model)
- ✅ SEMPRE que houver módulos distintos (ex: Auth, Projeto, Chat)
- ❌ Não use em diagramas de apenas 2–3 classes simples sem camadas
- ❌ Não use em diagramas de sequencia

---

## Diagrama de Sequência

```plantuml
@startuml
skinparam sequenceArrowThickness 2
skinparam roundcorner 10

actor "Usuário" as U
participant "Frontend" as FE
participant "AuthController" as AC
participant "SupabaseDAO" as DB

U -> FE: Clica em Login
FE -> AC: POST /auth/login {email, senha}
AC -> DB: verificar_credenciais(email, hash)
DB --> AC: {id, token}
AC --> FE: 200 OK {access_token}
FE --> U: Redireciona para Dashboard
@enduml
```

**Regras:**
- `actor` para humanos, `participant` para sistemas/serviços
- `->` síncrono, `-->` resposta / assíncrono
- Use `alt`/`else`/`end` para blocos condicionais

---

## Diagrama de Atividade

```plantuml
@startuml
skinparam activityBackgroundColor #E3F2FD
skinparam activityBorderColor #1976D2

start
:Receber Requisição;
if (Token válido?) then (sim)
  :Processar Lógica;
  if (Dados válidos?) then (sim)
    :Salvar no Banco;
    :Retornar 200 OK;
  else (não)
    :Retornar 422 Unprocessable;
  endif
else (não)
  :Retornar 401 Unauthorized;
endif
stop
@enduml
```

**Regras:**
- `start` / `stop` obrigatórios
- `:Ação;` — ponto e vírgula obrigatório no final
- `if (condição?) then (sim)` / `else (não)` / `endif`
- `fork` / `fork again` / `end fork` para fluxos paralelos

---

## Diagrama de Casos de Uso

```plantuml
@startuml
skinparam usecaseBackgroundColor #FFF9C4
skinparam usecaseBorderColor #F57F17

left to right direction

actor "Aluno" as A
actor "Professor" as P
actor "Admin" as AD

rectangle "IF ORBIT" {
  usecase "Cadastrar Projeto" as UC1
  usecase "Submeter para BraganTec" as UC2
  usecase "Avaliar Projeto" as UC3
  usecase "Gerar Relatório" as UC4
  usecase "Gerenciar Usuários" as UC5
}

A --> UC1
A --> UC2
P --> UC3
P --> UC4
AD --> UC5
UC2 .> UC1 : <<include>>
UC3 .> UC4 : <<extend>>
@enduml
```

---

## Diagrama ER (Entidade-Relacionamento)

```plantuml
@startuml
skinparam linetype ortho

entity "Usuario" as user {
  *id : UUID <<PK>>
  --
  nome : VARCHAR(100)
  email : VARCHAR(255) <<unique>>
  senha_hash : TEXT
}

entity "Projeto" as proj {
  *id : UUID <<PK>>
  --
  #usuario_id : UUID <<FK>>
  titulo : VARCHAR(200)
  descricao : TEXT
  status : ENUM
}

user ||--o{ proj : "cria"
@enduml
```

**Cardinalidade:**
- `||--||` (Exatamente um)
- `||--o{` (Um para zero ou muitos)
- `||--|{` (Um para um ou muitos)

---

## Mapa Mental (Mindmap)

```plantuml
@startmindmap
* Projeto Synapsis AI
** Visão Geral
*** Personalização em Tempo Real
*** Mentoria com Luna
** Tecnologias
*** Gemini 3 Flash
*** Supabase
** Metas
*** BraganTec 2026
*** Publicação Científica
@endmindmap
```

---

## Timeline (Linha do Tempo)

```plantuml
@startuml
robust "Fase do Projeto" as FP
concise "Marcos" as M

@FP
0 is Planejamento
+30 is Design
+60 is Desenvolvimento
+120 is Testes

@M
30 is "Design Finalizado"
60 is "Início Dev"
120 is "Beta Release"

@0 <-> @30 : {30 dias}
@enduml
```

---

## Padronização e Estilo

Sempre use este bloco de configuração inicial em diagramas complexos para garantir clareza:

```plantuml
skinparam linetype ortho
skinparam nodesep 60
skinparam ranksep 60
skinparam shadowing false
skinparam roundcorner 5

<style>
  diagramType {
    element {
      BackgroundColor #FFFFFF
      BorderColor #333333
      FontColor #333333
    }
  }
</style>
```

**Mudança de Direção (Setas Ocultas):**
Se você quiser forçar uma classe a ficar do lado da outra (horizontalmente) em vez de embaixo, você pode usar -left->, -right->, -up-> ou -down-> nos relacionamentos (ex: A -right-> B). Isso ajuda a moldar a "grade" do seu diagrama

**Regras:**
- `rectangle "Sistema" {}` delimita o sistema
- `-->` ator usa caso de uso
- `.>` com `<<include>>` (obrigatório) ou `<<extend>>` (opcional)

---

## Boas Práticas

- **Sempre use `package` quando houver camadas arquiteturais** (Controller, Service, DAO, Model, etc.)
- Sempre inclua `skinparam` para visual profissional
- Use sempre `skinparam linetype polyline`, `skinparam nodesep 50` e `skinparam ranksep 50` para que o diagrama fique com linhas retas e organizado.
- Nomes em português para elementos do domínio
- Máximo de 15-20 elementos por diagrama (legibilidade)
- Prefira diagramas focados a diagramas "completos demais"
- Após gerar, explique as principais relações ao usuário
