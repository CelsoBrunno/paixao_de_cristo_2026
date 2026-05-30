from io import BytesIO
from typing import Iterable, List, Tuple

from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


PAGE_WIDTH = 29.5 * cm
PAGE_HEIGHT = 21 * cm
MARGIN_X = 2.2 * cm
MARGIN_Y = 1.6 * cm
SECTION_GAP = 1.0 * cm
CARD_GAP = 0.7 * cm

PRIMARY_BROWN = colors.HexColor("#5E493D")
PRIMARY_DARK = colors.HexColor("#32251F")
GOLD = colors.HexColor("#D4AF37")
LIGHT_PARCHMENT = colors.HexColor("#F8F4EF")
WHITE = colors.white
GRAY_TEXT = colors.HexColor("#4A3A31")


def _draw_header(c: canvas.Canvas, title: str, subtitle: str) -> float:
    header_height = 4.6 * cm
    c.setFillColor(PRIMARY_BROWN)
    c.rect(0, PAGE_HEIGHT - header_height, PAGE_WIDTH, header_height, stroke=0, fill=1)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT - header_height / 2 + 0.6 * cm, title.upper())

    c.setFont("Helvetica", 12)
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT - header_height / 2 - 0.2 * cm, subtitle)

    return PAGE_HEIGHT - header_height - SECTION_GAP


def _draw_section_label(c: canvas.Canvas, x: float, y: float, text: str):
    c.setFont("Helvetica", 8.5)
    c.setFillColor(GOLD)
    c.drawString(x, y, text.upper())


def _draw_section_title(c: canvas.Canvas, x: float, y: float, text: str):
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(PRIMARY_BROWN)
    c.drawString(x, y, text)


def _draw_card(c: canvas.Canvas, x: float, y: float, w: float, h: float, title: str, body: Iterable[str]):
    c.setFillColor(WHITE)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.roundRect(x, y - h, w, h, 10, stroke=1, fill=1)

    c.setFillColor(PRIMARY_BROWN)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x + 0.5 * cm, y - 1.1 * cm, title)

    c.setFillColor(GRAY_TEXT)
    c.setFont("Helvetica", 9.5)
    text_y = y - 1.9 * cm
    for line in body:
        c.drawString(x + 0.5 * cm, text_y, line)
        text_y -= 0.5 * cm


def _draw_metric_card(c: canvas.Canvas, x: float, y: float, w: float, h: float, value: str, label: str):
    c.setFillColor(WHITE)
    c.setStrokeColor(colors.HexColor("#D9C9B7"))
    c.setLineWidth(1)
    c.roundRect(x, y - h, w, h, 12, stroke=1, fill=1)

    c.setFillColor(GOLD)
    c.circle(x + 0.7 * cm, y - 0.9 * cm, 0.35 * cm, stroke=0, fill=1)

    c.setFillColor(PRIMARY_BROWN)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(x + 1.4 * cm, y - 0.9 * cm + 0.2 * cm, value)

    c.setFillColor(GRAY_TEXT)
    c.setFont("Helvetica", 9.5)
    text_lines = label.split("\n")
    text_y = y - 1.8 * cm
    for line in text_lines:
        c.drawString(x + 0.7 * cm, text_y, line)
        text_y -= 0.45 * cm


def _draw_bullet_list(c: canvas.Canvas, x: float, y: float, items: List[Tuple[str, str]], width: float):
    c.setFillColor(WHITE)
    c.setStrokeColor(colors.HexColor("#E6D8C8"))
    c.setLineWidth(1)
    c.roundRect(x, y - 6.6 * cm, width, 6.6 * cm, 14, stroke=1, fill=1)

    text_y = y - 1.1 * cm
    for title, body in items:
        c.setFillColor(GOLD)
        c.circle(x + 0.7 * cm, text_y + 0.25 * cm, 0.25 * cm, stroke=0, fill=1)

        c.setFillColor(PRIMARY_BROWN)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(x + 1.3 * cm, text_y, title)

        c.setFillColor(GRAY_TEXT)
        c.setFont("Helvetica", 9.5)
        c.drawString(x + 1.3 * cm, text_y - 0.5 * cm, body)

        text_y -= 1.75 * cm


def _draw_pronac_pill(c: canvas.Canvas, center_x: float, y: float, text: str):
    pill_width = 8 * cm
    pill_height = 0.9 * cm
    c.setFillColor(colors.HexColor("#7A5D4C"))
    c.roundRect(center_x - pill_width / 2, y, pill_width, pill_height, 12, stroke=0, fill=1)

    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(center_x, y + 0.3 * cm, text.upper())


def _draw_contact_card(c: canvas.Canvas, x: float, y: float, width: float):
    height = 5.2 * cm
    c.setFillColor(WHITE)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.roundRect(x, y - height, width, height, 14, stroke=1, fill=1)

    c.setFillColor(PRIMARY_BROWN)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(x + 0.9 * cm, y - 1.1 * cm, "Vamos Conversar?")

    c.setFillColor(GRAY_TEXT)
    c.setFont("Helvetica", 10)
    text_lines = [
        "Alinhamos marketing, legado e impacto social ao projeto histórico de Maracanaú.",
        "",
        "Celso Brunno Rocha Custódio",
        "Proponente & Coordenador-Geral",
        "Projeto Paixão de Cristo de Maracanaú",
        "",
        "Patrimônio Cultural de Maracanaú (Lei Municipal Nº 2.710/2018)",
        "PRONAC Aprovado Nº 255599",
        "",
        "Celular: (85) 92002-1207",
        "Link rápido: https://paixaodecristomaracanau.pythonanywhere.com/seja-patrocinador",
        "E-mail: contato@teatroalmirdutra.com.br",
    ]
    text_y = y - 1.9 * cm
    for line in text_lines:
        c.drawString(x + 0.9 * cm, text_y, line)
        text_y -= 0.45 * cm


def generate_folheto_pdf() -> bytes:
    """Gera o PDF do folheto de patrocinadores com base no layout aprovado."""
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))

    # Página 1
    y = _draw_header(
        pdf,
        "Projeto Paixão de Cristo de Maracanaú",
        "O Maior Patrimônio Cultural de Maracanaú. 46 anos de história e impacto social."
    )

    _draw_section_label(pdf, MARGIN_X, y, "Projeto Cultural")
    _draw_section_title(pdf, MARGIN_X, y - 0.7 * cm, "Credibilidade Inquestionável")

    card_width = (PAGE_WIDTH - 2 * MARGIN_X - 2 * CARD_GAP) / 3
    card_height = 3.6 * cm
    credibility = [
        ("46ª edição tradicional", ["Espetáculo a céu aberto ativo há 46 anos,", "referência cultural do Ceará."]),
        ("Patrimônio oficial", ["Reconhecido pela Lei Municipal Nº 2.710/2018", "e calendário oficial de Maracanaú."]),
        ("100% gratuito e acessível", ["Acesso democrático com Libras,", "audiodescrição e áreas reservadas."]),
    ]
    card_y = y - 1.6 * cm
    for idx, (title, lines) in enumerate(credibility):
        card_x = MARGIN_X + idx * (card_width + CARD_GAP)
        _draw_card(pdf, card_x, card_y, card_width, card_height, title, lines)

    y = card_y - card_height - 1.0 * cm
    _draw_section_label(pdf, MARGIN_X, y, "Impacto Direto")
    _draw_section_title(pdf, MARGIN_X, y - 0.7 * cm, "Números que Impressionam")

    metric_width = (PAGE_WIDTH - 2 * MARGIN_X - 2 * CARD_GAP) / 3
    metric_height = 3.5 * cm
    metrics = [
        ("+30.000", "Espectadores presenciais"),
        ("+300", "Artistas e técnicos locais"),
        ("100", "Vagas gratuitas em oficinas"),
        ("+50", "Profissionais da cultura contratados"),
        ("+16", "Artesãos e bandas fomentados"),
        ("Live", "Transmissão ao vivo e mídia regional"),
    ]

    metric_y = y - 1.6 * cm
    for idx, (value, label) in enumerate(metrics):
        col = idx % 3
        row = idx // 3
        card_x = MARGIN_X + col * (metric_width + CARD_GAP)
        card_y_pos = metric_y - row * (metric_height + 0.7 * cm)
        _draw_metric_card(pdf, card_x, card_y_pos, metric_width, metric_height, value, label)

    y = metric_y - 2 * (metric_height + 0.7 * cm) - 1.0 * cm
    _draw_section_label(pdf, MARGIN_X, y, "ESG & Marketing")
    _draw_section_title(pdf, MARGIN_X, y - 0.7 * cm, "Uma Plataforma Completa")

    bullet_items = [
        ("Visibilidade massiva", "Exposição direta para 30.000 pessoas, com cobertura regional e transmissão."),
        ("Impacto social ESG", "Geração de renda, formação gratuita e fortalecimento da comunidade local."),
        ("Legado e reputação", "Associe sua marca a um patrimônio cultural reconhecido por lei."),
    ]
    _draw_bullet_list(pdf, MARGIN_X, y - 1.6 * cm, bullet_items, PAGE_WIDTH - 2 * MARGIN_X)

    pdf.setFont("Helvetica", 9)
    pdf.setFillColor(PRIMARY_BROWN)
    pdf.drawCentredString(PAGE_WIDTH / 2, 1.0 * cm, "Projeto Paixão de Cristo de Maracanaú • Folheto para Patrocinadores • Página 1 de 2")

    pdf.showPage()

    # Página 2
    y = _draw_header(
        pdf,
        "Uma Oportunidade Estratégica para Sua Marca",
        "100% de incentivo fiscal. 0% de custo."
    )

    pdf.setFont("Helvetica", 10.5)
    pdf.setFillColor(GRAY_TEXT)
    pdf.drawCentredString(
        PAGE_WIDTH / 2,
        y - 0.3 * cm,
        "Projeto aprovado na Lei de Incentivo à Cultura (PRONAC 255599). Empresas do Lucro Real destinam até 4% do IRPJ com dedução total."
    )
    pdf.drawCentredString(
        PAGE_WIDTH / 2,
        y - 0.9 * cm,
        "Marketing, legado e ESG com custo fiscal zero."
    )
    _draw_pronac_pill(pdf, PAGE_WIDTH / 2, y - 1.7 * cm, "Projeto aprovado PRONAC 255599")

    y = y - 3.2 * cm

    _draw_section_label(pdf, MARGIN_X, y, "Cotas Disponíveis")
    _draw_section_title(pdf, MARGIN_X, y - 0.7 * cm, "Cotas de Patrocínio")

    sponsorship_cards = [
        (
            '"Apresenta"',
            "R$ 250.000,00",
            [
                "Naming rights completo do espetáculo.",
                "Visibilidade máxima em palco, peças e transmissão.",
                "Ativações exclusivas, oficinas e acessibilidade com a marca.",
                "Uso do banco de imagens e citações oficiais.",
            ],
        ),
        (
            '"Patrocina" (2 cotas)',
            "R$ 200.000,00",
            [
                "Marca nas estruturas principais e telões.",
                "Presença na transmissão ao vivo e mídia espontânea.",
                "Ativações na Feira Livre e experiências com o público.",
                "Logotipo na cobertura audiovisual do espetáculo.",
            ],
        ),
        (
            '"Apoio"',
            "R$ 40.000,00",
            [
                "Marca nas estruturas de apoio e materiais oficiais.",
                "Menções em redes sociais e releases para imprensa.",
                "Atuação em eventos paralelos e relacionamento.",
                "Créditos na transmissão e gravação oficial.",
            ],
        ),
        (
            '"Apoio Cultural"',
            "R$ 9.554,00",
            [
                "Visibilidade nas ativações territoriais e comunicação local.",
                "Associação a ações sociais e reconhecimento comunitário.",
                "Agradecimentos em mídias digitais e transmissão online.",
                "Participação em momentos especiais com público e elenco.",
            ],
        ),
    ]

    card_width = (PAGE_WIDTH - 2 * MARGIN_X - CARD_GAP) / 2
    card_height = 6.4 * cm
    start_y = y - 1.6 * cm
    for idx, (title, value, items) in enumerate(sponsorship_cards):
        col = idx % 2
        row = idx // 2
        x_pos = MARGIN_X + col * (card_width + CARD_GAP)
        y_pos = start_y - row * (card_height + 0.8 * cm)

        pdf.setFillColor(WHITE)
        pdf.setStrokeColor(GOLD)
        pdf.setLineWidth(1.2)
        pdf.roundRect(x_pos, y_pos - card_height, card_width, card_height, 12, stroke=1, fill=1)

        pdf.setFont("Helvetica-Bold", 12)
        pdf.setFillColor(PRIMARY_BROWN)
        pdf.drawString(x_pos + 0.7 * cm, y_pos - 1.0 * cm, title)

        pdf.setFont("Helvetica-Bold", 14)
        pdf.setFillColor(GOLD)
        pdf.drawString(x_pos + 0.7 * cm, y_pos - 1.8 * cm, value)

        pdf.setFont("Helvetica", 9.5)
        pdf.setFillColor(GRAY_TEXT)
        bullet_y = y_pos - 2.4 * cm
        for item in items:
            pdf.circle(x_pos + 0.7 * cm, bullet_y + 0.15 * cm, 0.15 * cm, stroke=0, fill=1)
            pdf.drawString(x_pos + 1.1 * cm, bullet_y, item)
            bullet_y -= 0.55 * cm

    _draw_contact_card(pdf, MARGIN_X, 6.8 * cm, PAGE_WIDTH - 2 * MARGIN_X)

    pdf.setFont("Helvetica", 9)
    pdf.setFillColor(PRIMARY_BROWN)
    pdf.drawCentredString(PAGE_WIDTH / 2, 1.0 * cm, "Projeto Paixão de Cristo de Maracanaú • Folheto para Patrocinadores • Página 2 de 2")

    pdf.showPage()
    pdf.save()

    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes


