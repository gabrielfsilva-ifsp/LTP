

import requests

BASE_URL = "http://127.0.0.1:5001"


def print_resultado(titulo, sucesso, status_code=None, resposta=None):
    status_str = "[ PASSOU ]" if sucesso else "[ FALHOU ]"
    print(f"\n{status_str} — {titulo}")
    if status_code is not None:
        print(f"         Status Code: {status_code}")
    if resposta is not None:
        resp_str = str(resposta)
        if len(resp_str) > 300:
            resp_str = resp_str[:300] + "..."
        print(f"         Resposta: {resp_str}")


def main():
    print("=======================================================")
    print("  Iniciando testes de integração das rotas da API LTP")
    print("=======================================================")

    print(f"Verificando servidor ativo em: {BASE_URL}")

    novo_projeto_id = None
    nova_amizade_id = None

    res = requests.get(f"{BASE_URL}/api/projetos")
    if res.status_code == 200 and isinstance(res.json(), list):
        print_resultado("Listagem de Projetos (GET /api/projetos)", True, res.status_code, f"Carregados {len(res.json())} projetos.")
    else:
        print_resultado("Listagem de Projetos (GET /api/projetos)", False, res.status_code, res.text)

    payload_proj = {
        "nome": "Dispositivo IoT de Detecção de Vazamento de Gás",
        "categoria": "engenharias",
        "resumo": "Protótipo utilizando sensor MQ-2 e ESP32 para identificar vazamentos domésticos de gás GLP.",
        "objetivo_geral": "Desenvolver um sistema autônomo de baixo custo para prevenção de acidentes residenciais.",
    }
    res = requests.post(f"{BASE_URL}/api/projetos", json=payload_proj)
    if res.status_code == 201:
        data = res.json()
        novo_projeto_id = data.get("id")
        print_resultado("Criação de Projeto (POST /api/projetos)", True, res.status_code, data)
    else:
        print_resultado("Criação de Projeto (POST /api/projetos)", False, res.status_code, res.text)

    if novo_projeto_id:
        res = requests.get(f"{BASE_URL}/api/projetos/{novo_projeto_id}")
        if res.status_code == 200:
            print_resultado("Busca de Projeto por ID (GET /api/projetos/<id>)", True, res.status_code, res.json())
        else:
            print_resultado("Busca de Projeto por ID (GET /api/projetos/<id>)", False, res.status_code, res.text)

    if novo_projeto_id:
        payload_update = {
            "status": "em_andamento",
            "metodologia": "Uso de ESP32 programado in C++ através da IDE do Arduino + Sensor MQ-2 calibrado.",
        }
        res = requests.put(f"{BASE_URL}/api/projetos/{novo_projeto_id}", json=payload_update)
        if res.status_code == 200:
            print_resultado("Atualização de Projeto (PUT /api/projetos/<id>)", True, res.status_code, res.json())
        else:
            print_resultado("Atualização de Projeto (PUT /api/projetos/<id>)", False, res.status_code, res.text)

    if novo_projeto_id:
        res_get = requests.get(f"{BASE_URL}/api/projetos/{novo_projeto_id}")
        if res_get.status_code == 200:
            projeto_dados = res_get.json()
            res_pdf = requests.post(f"{BASE_URL}/api/pdf/exportar", json=projeto_dados)
            if res_pdf.status_code == 200 and res_pdf.headers.get("content-type") == "application/pdf":
                filename = "projeto_teste_exportado.pdf"
                with open(filename, "wb") as f:
                    f.write(res_pdf.content)
                print_resultado("Exportação de PDF (POST /api/pdf/exportar)", True, res_pdf.status_code, f"Arquivo salvo com sucesso como '{filename}'")
            else:
                print_resultado("Exportação de PDF (POST /api/pdf/exportar)", False, res_pdf.status_code, res_pdf.text)

    if novo_projeto_id:
        res = requests.delete(f"{BASE_URL}/api/projetos/{novo_projeto_id}")
        if res.status_code == 200:
            print_resultado("Remoção de Projeto (DELETE /api/projetos/<id>)", True, res.status_code, res.json())
        else:
            print_resultado("Remoção de Projeto (DELETE /api/projetos/<id>)", False, res.status_code, res.text)

    res = requests.get(f"{BASE_URL}/api/amizades")
    if res.status_code == 200 and isinstance(res.json(), list):
        print_resultado("Listagem de Amizades (GET /api/amizades)", True, res.status_code, f"Carregadas {len(res.json())} solicitações.")
    else:
        print_resultado("Listagem de Amizades (GET /api/amizades)", False, res.status_code, res.text)

    payload_amz = {
        "solicitante_id": "user-A",
        "alvo_id": "user-D",
    }
    res = requests.post(f"{BASE_URL}/api/amizades", json=payload_amz)
    if res.status_code == 201:
        data = res.json()
        nova_amizade_id = data.get("id")
        print_resultado("Solicitação de Amizade (POST /api/amizades)", True, res.status_code, data)
    else:
        print_resultado("Solicitação de Amizade (POST /api/amizades)", False, res.status_code, res.text)

    if nova_amizade_id:
        payload_status = {"status": "aceita"}
        res = requests.put(f"{BASE_URL}/api/amizades/{nova_amizade_id}", json=payload_status)
        if res.status_code == 200:
            print_resultado("Aceitar Solicitação (PUT /api/amizades/<id>)", True, res.status_code, res.json())
        else:
            print_resultado("Aceitar Solicitação (PUT /api/amizades/<id>)", False, res.status_code, res.text)

    if nova_amizade_id:
        res = requests.delete(f"{BASE_URL}/api/amizades/{nova_amizade_id}")
        if res.status_code == 200:
            print_resultado("Remoção de Amizade (DELETE /api/amizades/<id>)", True, res.status_code, res.json())
        else:
            print_resultado("Remoção de Amizade (DELETE /api/amizades/<id>)", False, res.status_code, res.text)

    print("\n[INFO] Testando Chatbot Luna (Gemini)...")
    payload_chat = {
        "prompt": "Olá Luna! me fale um projeto vencedor da bragantec"
    }
    res = requests.post(f"{BASE_URL}/api/chatbot/conversar", json=payload_chat, timeout=60)
    if res.status_code == 200:
        print_resultado("Chatbot Luna (POST /api/chatbot/conversar)", True, res.status_code, res.json())
    else:
        print_resultado("Chatbot Luna (POST /api/chatbot/conversar)", False, res.status_code, res.json() if res.headers.get("content-type") == "application/json" else res.text)

    print("\n[INFO] Testando Gerador de Projetos via IA (Gemini)...")
    payload_gerador = {
        "tema": "Detector de Pragas em Plantações de Café usando Visão Computacional",
        "categoria": "informatica",
    }
    res = requests.post(f"{BASE_URL}/api/projetos/gerar", json=payload_gerador, timeout=150)
    if res.status_code == 201:
        print_resultado("Gerador de Projetos via IA (POST /api/projetos/gerar)", True, res.status_code, res.json())
    else:
        print_resultado("Gerador de Projetos via IA (POST /api/projetos/gerar)", False, res.status_code, res.json() if res.headers.get("content-type") == "application/json" else res.text)

    print("\n=======================================================")
    print("  Fim dos testes de integração das rotas.")
    print("=======================================================")


if __name__ == "__main__":
    main()
