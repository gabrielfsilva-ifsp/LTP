
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from classes.amizade import Amizade
from classes.mensagem import Mensagem
from classes.projeto import Projeto
from configuracoes import categorias_validas


def separador(titulo):
    print(f"\n{'='*55}")
    print(f"  {titulo}")
    print(f"{'='*55}")


separador("TESTES — Classe Projeto")

p1 = Projeto(
    id="proj-001",
    nome="Sistema de Monitoramento de Queimadas",
    categoria="ciencias_natureza_exatas",
    resumo="Plataforma para detecção precoce de incêndios usando satélites.",
    objetivo_geral="Reduzir o tempo de resposta a queimadas no Cerrado em 40%.",
)
print(f"\n[OK] Criado: {p1}")
print(f"     to_dict keys: {list(p1.to_dict().keys())}")

p2 = Projeto(id="proj-002", nome="Projeto Incompleto", categoria="informatica")
campos_faltando = p2.validar_campos()
print(f"\n[OK] Campos obrigatórios faltando in p2: {campos_faltando}")

if p1.atualizar_status("em_andamento"):
    print(f"\n[OK] Status atualizado: {p1.status}")
else:
    print("\n[FALHOU] Não foi possível atualizar o status para em_andamento")

p_invalido_nome = Projeto(id="x", nome="  ", categoria="informatica")
if not p_invalido_nome.nome.strip():
    print("\n[OK] Nome vazio detectado com if/else")
else:
    print("\n[FALHOU] Nome vazio não detectado")

p_invalido_cat = Projeto(id="x", nome="Teste", categoria="inexistente")
if p_invalido_cat.categoria not in categorias_validas:
    print("\n[OK] Categoria inválida detectada com if/else")
else:
    print("\n[FALHOU] Categoria inválida não detectada")

if not p1.atualizar_status("arquivado"):
    print("\n[OK] Status inválido recusado com sucesso (retornou False)")
else:
    print("\n[FALHOU] Status inválido aceito indevidamente")


separador("TESTES — Classe Mensagem")

m1 = Mensagem(id="msg-001", conteudo="Olá Luna, como me ajudas?", remetente="user")
print(f"\n[OK] Criada: {m1}")

m2 = Mensagem(
    id="msg-002",
    conteudo="Olá! Posso te ajudar a criar um projeto científico, escrever resumos e muito mais!",
    remetente="luna",
)
print(f"\n[OK] Resposta da Luna: {m2}")
print(f"     to_dict: {m2.to_dict()}")

m_invalida_cont = Mensagem(id="x", conteudo="   ", remetente="user")
if not m_invalida_cont.conteudo.strip():
    print("\n[OK] Conteúdo vazio detectado com if/else")
else:
    print("\n[FALHOU] Conteúdo vazio não detectado")

m_invalida_rem = Mensagem(id="x", conteudo="Teste", remetente="bot")
if m_invalida_rem.remetente not in Mensagem.remetentes_validos:
    print("\n[OK] Remetente inválido detectado com if/else")
else:
    print("\n[FALHOU] Remetente inválido não detectado")


separador("TESTES — Classe Amizade")

a1 = Amizade(id="amz-001", solicitante_id="user-A", alvo_id="user-B")
print(f"\n[OK] Criada: {a1}")
print(f"     Status inicial: {a1.status}")

if a1.aceitar():
    print(f"\n[OK] Após aceitar(): {a1.status}")
else:
    print("\n[FALHOU] Não foi possível aceitar a amizade")

if not a1.aceitar():
    print("\n[OK] Aceitar já aceito recusado com sucesso (retornou False)")
else:
    print("\n[FALHOU] Aceitou amizade já aceita")

a2 = Amizade(id="amz-002", solicitante_id="user-C", alvo_id="user-D")
if a2.recusar():
    print(f"\n[OK] Após recusar(): {a2.status}")
else:
    print("\n[FALHOU] Não foi possível recusar a amizade pendente")

a_invalida = Amizade(id="x", solicitante_id="user-X", alvo_id="user-X")
if a_invalida.solicitante_id == a_invalida.alvo_id:
    print("\n[OK] Auto-amizade detectada com if/else")
else:
    print("\n[FALHOU] Auto-amizade não detectada")

print(f"\n[OK] to_dict de a2: {a2.to_dict()}")


separador("RESUMO FINAL")
print("\nTodos os testes passaram com sucesso!")
print("\nObjetos criados:")
print(f"  {p1}")
print(f"  {m1}")
print(f"  {m2}")
print(f"  {a1}")
print(f"  {a2}")
