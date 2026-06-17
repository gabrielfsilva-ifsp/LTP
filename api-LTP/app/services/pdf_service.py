
import html
import io
import os
import re

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


class PdfService:

    def __init__(self):
        self.assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets")

    def _limpar_html_para_texto(self, texto):
        if not texto:
            return ""
        texto = str(texto)
        texto = re.sub(r'(?i)<br\s*/?>', '\n', texto)
        texto = re.sub(r'(?i)<li>', '\n- ', texto)
        texto = re.sub(r'(?i)</p>', '\n\n', texto)
        texto = re.sub(r'<[^>]+>', '', texto)
        return texto.strip()

    def gerar_pdf_projeto(self, dados_projeto):
        if not dados_projeto:
            return None, "Nenhum dado de projeto recebido."
        return self._gerar_pdf_interno(dados_projeto), None

    def _gerar_pdf_interno(self, dados):
        buffer = io.BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=2.0 * cm,
            leftMargin=2.0 * cm,
            topMargin=2.6 * cm,
            bottomMargin=2.0 * cm,
        )

        estilos = getSampleStyleSheet()
        estilo_corpo = ParagraphStyle(
            "Corpo", parent=estilos["Normal"],
            fontSize=10, leading=14, textColor=colors.red,
            wordWrap='CJK', splitLongWords=True,
        )
        estilo_titulo_caixa = ParagraphStyle(
            "T_BOX", parent=estilos["Normal"],
            fontSize=10, fontName="Helvetica-Bold", spaceAfter=4,
            textTransform='uppercase', textColor=colors.black, splitLongWords=True,
        )
        estilo_titulo_grande = ParagraphStyle(
            "T_BIG", parent=estilos["Normal"],
            fontSize=14, fontName="Helvetica-Bold", alignment=1,
            spaceAfter=12, textTransform='uppercase', textColor=colors.black, splitLongWords=True,
        )
        estilo_plano_info = ParagraphStyle(
            "P_INFO", parent=estilos["Normal"],
            fontSize=8, alignment=1, spaceAfter=20,
            fontName="Helvetica-Bold", textColor=colors.red, splitLongWords=True,
        )
        estilo_alerta = ParagraphStyle(
            "T_ALERT", parent=estilos["Normal"],
            fontSize=8, alignment=1, textColor=colors.red,
            textTransform='uppercase', splitLongWords=True,
        )
        estilo_pequeno = ParagraphStyle(
            "T_SMALL", parent=estilos["Normal"],
            fontSize=8, leading=10, textColor=colors.black,
            textTransform='uppercase', splitLongWords=True,
        )
        estilo_termo = ParagraphStyle(
            "T_TERMO", parent=estilos["Normal"],
            fontSize=8, alignment=4, leading=11, textColor=colors.black,
            fontName="Helvetica-Bold", textTransform='uppercase', splitLongWords=True,
        )

        def cabecalho(canvas, document):
            canvas.saveState()
            caminho_banner = os.path.join(self.assets_dir, "bannerpdf.jpg")
            if os.path.exists(caminho_banner):
                canvas.drawImage(
                    caminho_banner, 0, A4[1] - 3.2 * cm,
                    width=A4[0], height=3.2 * cm,
                    preserveAspectRatio=True, anchor='n',
                )
            canvas.restoreState()

        def criar_tabela_caixa(titulo, conteudo, width=17 * cm, estilo=estilo_corpo):
            titulo_str = str(titulo) if titulo is not None else ""
            elementos_caixa = [
                Paragraph(f"<b>{html.escape(titulo_str)}:</b>", estilo_titulo_caixa),
                Spacer(1, 4),
            ]

            if isinstance(conteudo, list):
                if not conteudo:
                    elementos_caixa.append(Paragraph("&nbsp;", estilo))
                for item in conteudo:
                    if isinstance(item, str):
                        item = self._limpar_html_para_texto(item)
                        safe_val = html.escape(item).replace('\n', '<br/>')
                        if not safe_val.strip():
                            safe_val = "&nbsp;"
                        elementos_caixa.append(Paragraph(safe_val, estilo))
                    elif item is None:
                        elementos_caixa.append(Paragraph("&nbsp;", estilo))
                    else:
                        elementos_caixa.append(item)
            elif isinstance(conteudo, str):
                conteudo = self._limpar_html_para_texto(conteudo)
                safe_str = html.escape(conteudo).replace('\n', '<br/>')
                if not safe_str.strip():
                    safe_str = "&nbsp;"
                elementos_caixa.append(Paragraph(safe_str, estilo))
            elif conteudo is None:
                elementos_caixa.append(Paragraph("&nbsp;", estilo))
            else:
                elementos_caixa.append(conteudo)

            t = Table([[elementos_caixa]], colWidths=[width])
            t.setStyle(TableStyle([
                ('BOX', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('PADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            return t

        elementos = []

        elementos.append(criar_tabela_caixa("TÍTULO DO PROJETO", dados.get("nome", "")))
        elementos.append(Spacer(1, 10))

        categorias_display = [
            "Ciências da Natureza e Exatas",
            "Informática",
            "Ciências Humanas e Linguagens",
            "Engenharias",
        ]
        projeto_cat = str(dados.get("categoria", ""))
        cat_items = []
        for c in categorias_display:
            x_mark = "x" if c.lower() in projeto_cat.lower() or projeto_cat.lower().replace("_", " ") in c.lower() else " "
            cat_items.append(f"( {x_mark} ) {c}")

        estilo_corpo_preto = ParagraphStyle(
            "CorpoPreto", parent=estilos["Normal"],
            fontSize=10, leading=14, textColor=colors.black,
        )
        elementos.append(criar_tabela_caixa("CATEGORIA (MARCAR APENAS UMA)", cat_items, estilo=estilo_corpo_preto))
        elementos.append(Spacer(1, 10))

        elementos.append(criar_tabela_caixa("RESUMO", dados.get("resumo", "")))
        elementos.append(Spacer(1, 10))

        palavras_chave = dados.get("palavras_chave", "")
        if isinstance(palavras_chave, list):
            palavras_chave = ", ".join(palavras_chave)
        elementos.append(criar_tabela_caixa("PALAVRAS-CHAVE", palavras_chave))
        elementos.append(Spacer(1, 20))

        elementos.append(Paragraph("<u>PLANO DE PESQUISA</u>", estilo_titulo_grande))
        msg_plano = (
            "O PLANO DE PESQUISA É O PLANEJAMENTO INICIAL DO QUE SERÁ EXECUTADO EM SUA PESQUISA. "
            "DEVE CONTER O OBJETIVO OU HIPÓTESE DA PESQUISA E OS MÉTODOS QUE SERÃO UTILIZADOS "
            "PARA SE ALCANÇAR ESSES OBJETIVOS."
        )
        elementos.append(Paragraph(msg_plano, estilo_plano_info))

        elementos.append(criar_tabela_caixa("INTRODUÇÃO", dados.get("introducao", "")))
        elementos.append(Spacer(1, 10))

        objetivos_conteudo = []
        obj_geral = dados.get("objetivo_geral", "")
        if obj_geral:
            objetivos_conteudo.append(f"<b>Objetivo Geral:</b> {html.escape(str(obj_geral))}")
            objetivos_conteudo.append(Spacer(1, 4))

        obj_esp = dados.get("objetivos_especificos") or []
        if obj_esp:
            objetivos_conteudo.append("<b>Objetivos Específicos:</b>")
            for i, obj in enumerate(obj_esp, 1):
                if obj is not None:
                    objetivos_conteudo.append(f"{i}. {html.escape(str(obj))}")

        if not objetivos_conteudo:
            objetivos_conteudo = ""

        elementos.append(criar_tabela_caixa("OBJETIVOS", objetivos_conteudo))
        elementos.append(Spacer(1, 10))

        elementos.append(criar_tabela_caixa("METODOLOGIA", dados.get("metodologia", "")))
        elementos.append(Spacer(1, 10))

        cronograma = dados.get("cronograma") or {}
        meses_cabecalho = ["Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov"]
        dados_tabela_crono = [["Etapa\nDefinição do tema"] + meses_cabecalho]

        estilo_p_t = ParagraphStyle(
            "P_T", parent=estilos["Normal"],
            fontSize=8, leading=10, wordWrap='CJK', splitLongWords=True,
        )

        if isinstance(cronograma, dict) and "atividades" in cronograma:
            for atv in cronograma["atividades"]:
                if isinstance(atv, dict):
                    fase = html.escape(str(atv.get("nome", atv.get("fase", ""))))
                    row = [Paragraph(fase, estilo_p_t)]
                    meses_atv = atv.get("meses", [])
                    for m in range(3, 12):
                        if isinstance(meses_atv, list) and (m in meses_atv or str(m) in meses_atv):
                            row.append("x")
                        else:
                            row.append("")
                    dados_tabela_crono.append(row)
        else:
            dados_tabela_crono.append([
                Paragraph("Ver dados no sistema online", estilo_p_t),
                "", "", "", "", "", "", "", "", "",
            ])

        t_crono = Table(dados_tabela_crono, colWidths=[5.3 * cm] + [1.2 * cm] * 9)
        t_crono.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]))

        elementos.append(criar_tabela_caixa("CRONOGRAMA", t_crono))
        elementos.append(Spacer(1, 10))

        elementos.append(criar_tabela_caixa("RESULTADOS ESPERADOS", dados.get("resultados_esperados", "")))
        elementos.append(Spacer(1, 10))

        refs = dados.get("referencias_bibliograficas", "")
        elementos.append(criar_tabela_caixa("REFERÊNCIAS BIBLIOGRÁFICAS", refs))
        elementos.append(Spacer(1, 20))

        elementos.append(Paragraph("<u>CONTINUAÇÃO DE PROJETO ANTERIOR</u>", estilo_titulo_grande))
        elementos.append(Paragraph(
            "*PREENCHIMENTO OBRIGATÓRIO APENAS PROJETOS QUE SÃO CONTINUIDADE DE PROJETO ANTERIORES",
            estilo_alerta,
        ))
        elementos.append(Spacer(1, 10))

        elementos.append(criar_tabela_caixa("TÍTULO DO PROJETO DE PESQUISA ANTERIOR", ""))
        elementos.append(Spacer(1, 10))
        elementos.append(criar_tabela_caixa("RESUMO DO PROJETO DE PESQUISA ANTERIOR", "", width=17 * cm))
        elementos.append(Spacer(1, 10))

        caixa_periodo = [
            Paragraph("<b>PERÍODO DE DESENVOLVIMENTO DO PROJETO DE PESQUISA ANTERIOR:</b>", estilo_titulo_caixa),
            Spacer(1, 8),
            Paragraph("<b>INÍCIO:</b>", estilo_pequeno),
            Spacer(1, 8),
            Paragraph("<b>TÉRMINO:</b>", estilo_pequeno),
            Spacer(1, 8),
        ]
        t_periodo = Table([[caixa_periodo]], colWidths=[17 * cm])
        t_periodo.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        elementos.append(t_periodo)
        elementos.append(Spacer(1, 20))

        termo_txt = (
            "AO INSCREVER O PROJETO CONCORDAMOS COM O REGULAMENTO DA 15ª BRAGANTEC E DECLARAMOS "
            "QUE AS INFORMAÇÕES ACIMA ESTÃO CORRETAS E O RESUMO E PÔSTER REFLETEM APENAS O TRABALHO "
            "REALIZADO AO LONGO DOS ÚLTIMOS 12 (DOZE) MESES. ESTAMOS CIENTES DE QUE A NÃO VERACIDADE "
            "DAS INFORMAÇÕES FORNECIDAS PODERÁ IMPLICAR NA DESCLASSIFICAÇÃO DO PROJETO."
        )
        elementos.append(Paragraph(termo_txt, estilo_termo))

        doc.build(elementos, onFirstPage=cabecalho, onLaterPages=cabecalho)

        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes


pdf_service = PdfService()
