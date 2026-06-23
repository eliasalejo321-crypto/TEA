# -*- coding: utf-8 -*-
"""Genera el PDF académico con maquetación cuidada.
Portada + Agradecimientos + Índice + Introducción + Planteamiento + Capítulo 3.
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib import colors
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Image,
    NextPageTemplate, PageBreak, Table, TableStyle, HRFlowable, KeepTogether,
)
from reportlab.lib.styles import ParagraphStyle

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")
CONTENT = os.path.join(BASE, "content")
OUT = os.path.join(BASE, "Tesis_Introduccion_y_Planteamiento.pdf")

# ---- Paleta ----
AZUL = colors.HexColor("#0A2342")     # azul institucional
GOLD = colors.HexColor("#9C7A3C")     # dorado de acento
PERG = colors.HexColor("#F6F3EC")     # fondo pergamino para citas
GRIS = colors.HexColor("#6B6B6B")
TINTA = colors.HexColor("#1A1A1A")

# ---- Datos de portada ----
NOMBRE_SUSTENTANTE = "ELÍAS ALEJO CEDILLO"

RUN_TITLE = "Naturaleza jurídica de las representaciones y garantías en el SPA"


def hyph(style):
    """Activa separación silábica en español (si pyphen está disponible)."""
    try:
        style.hyphenationLang = "es_ES"
    except Exception:
        pass
    return style


# ---------- Estilos de cuerpo ----------
body = hyph(ParagraphStyle("body", fontName="Times-Roman", fontSize=12, leading=18,
                           alignment=TA_JUSTIFY, firstLineIndent=1.25 * cm, textColor=TINTA))
research_q = hyph(ParagraphStyle("rq", fontName="Times-Italic", fontSize=12, leading=18,
                                 alignment=TA_JUSTIFY, firstLineIndent=0, leftIndent=1.0 * cm,
                                 rightIndent=1.0 * cm, textColor=TINTA))
agra = hyph(ParagraphStyle("agra", fontName="Times-Roman", fontSize=12, leading=19,
                           alignment=TA_JUSTIFY, firstLineIndent=1.25 * cm, spaceAfter=6, textColor=TINTA))
quote_txt = hyph(ParagraphStyle("quote_txt", fontName="Times-Italic", fontSize=11, leading=15.5,
                                alignment=TA_JUSTIFY, textColor=colors.HexColor("#33312B")))

# Encabezados de sección / capítulo
section = ParagraphStyle("section", fontName="Times-Bold", fontSize=15, leading=20,
                         alignment=TA_CENTER, spaceBefore=4, spaceAfter=2, textColor=AZUL)
chap_kicker = ParagraphStyle("chap_kicker", fontName="Times-Bold", fontSize=11, leading=14,
                             alignment=TA_CENTER, textColor=GOLD, spaceAfter=2)
chap_num = ParagraphStyle("chap_num", fontName="Times-Bold", fontSize=22, leading=26,
                          alignment=TA_CENTER, textColor=AZUL, spaceAfter=2)
chapsub = ParagraphStyle("chapsub", fontName="Times-Bold", fontSize=12.5, leading=17,
                         alignment=TA_CENTER, spaceBefore=2, spaceAfter=18, textColor=TINTA)
subsec = ParagraphStyle("subsec", fontName="Times-Bold", fontSize=12.5, leading=16,
                        alignment=TA_LEFT, spaceBefore=15, spaceAfter=5, textColor=AZUL)

# Portada
c_inst = ParagraphStyle("c_inst", fontName="Times-Bold", fontSize=14.5, leading=18, alignment=TA_CENTER, textColor=AZUL)
c_fac = ParagraphStyle("c_fac", fontName="Times-Bold", fontSize=12.5, leading=16, alignment=TA_CENTER, textColor=AZUL)
c_sub = ParagraphStyle("c_sub", fontName="Times-Roman", fontSize=11.5, leading=15, alignment=TA_CENTER, textColor=GRIS)
c_title = ParagraphStyle("c_title", fontName="Times-Bold", fontSize=14.5, leading=20, alignment=TA_CENTER, textColor=TINTA)
c_mod = ParagraphStyle("c_mod", fontName="Times-Roman", fontSize=12, leading=18, alignment=TA_CENTER, textColor=TINTA)
c_modb = ParagraphStyle("c_modb", fontName="Times-Bold", fontSize=13, leading=18, alignment=TA_CENTER, textColor=AZUL)
c_name = ParagraphStyle("c_name", fontName="Times-Bold", fontSize=13.5, leading=18, alignment=TA_CENTER, textColor=AZUL)

# Agradecimientos / índice
agra_title = ParagraphStyle("agra_title", fontName="Times-Bold", fontSize=15, leading=20, alignment=TA_CENTER, textColor=AZUL)
idx_title = ParagraphStyle("idx_title", fontName="Times-Bold", fontSize=15, leading=20, alignment=TA_CENTER, textColor=AZUL)
idx_l0 = ParagraphStyle("idx_l0", fontName="Times-Bold", fontSize=11, leading=15, alignment=TA_LEFT, textColor=AZUL)
idx_l1 = ParagraphStyle("idx_l1", fontName="Times-Roman", fontSize=11, leading=15, alignment=TA_LEFT, leftIndent=0.8 * cm, textColor=TINTA)
idx_pg = ParagraphStyle("idx_pg", fontName="Times-Bold", fontSize=11, leading=15, alignment=TA_RIGHT, textColor=TINTA)
idx_pend = ParagraphStyle("idx_pend", fontName="Times-Italic", fontSize=8.5, leading=15, alignment=TA_RIGHT, textColor=GRIS)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def read_blocks(path):
    with open(path, encoding="utf-8") as f:
        raw = f.read().strip()
    return [b.strip() for b in raw.split("\n\n") if b.strip()]


def rule(width="38%", color=GOLD, thick=1.1, sb=3, sa=14):
    return HRFlowable(width=width, thickness=thick, color=color, spaceBefore=sb,
                      spaceAfter=sa, hAlign="CENTER", lineCap="round")


def heading(text, anchor=None):
    """Encabezado de sección centrado con filete dorado."""
    return [Paragraph(text, section), rule()]


def quote_box(text):
    """Cita textual de ley: barra azul a la izquierda + fondo pergamino."""
    inner = Paragraph(esc(text), quote_txt)
    t = Table([["", inner]], colWidths=[0.16 * cm, None])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), AZUL),
        ("BACKGROUND", (1, 0), (1, 0), PERG),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (1, 0), (1, 0), 12),
        ("RIGHTPADDING", (1, 0), (1, 0), 12),
        ("TOPPADDING", (1, 0), (1, 0), 8),
        ("BOTTOMPADDING", (1, 0), (1, 0), 8),
        ("LEFTPADDING", (0, 0), (0, 0), 0),
        ("RIGHTPADDING", (0, 0), (0, 0), 0),
    ]))
    return Table([[t]], colWidths=[None],
                 style=[("LEFTPADDING", (0, 0), (-1, -1), 18),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                        ("TOPPADDING", (0, 0), (-1, -1), 4),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 6)])


# Estructura del índice
TOC = [
    (0, "AGRADECIMIENTOS", "AGRADECIMIENTOS"),
    (0, "INTRODUCCIÓN", "I. INTRODUCCIÓN"),
    (0, "PLANTEAMIENTO DEL PROBLEMA", "II. PLANTEAMIENTO DEL PROBLEMA"),
    (1, "Pregunta de investigación", None),
    (0, "CAPÍTULO PRIMERO. EL SPA Y SU FUNCIÓN EN LAS FUSIONES Y ADQUISICIONES", None),
    (1, "1.1 Concepto y caracteres del Share Purchase Agreement", None),
    (1, "1.2 Estructura: declaraciones y garantías, covenants, condiciones e indemnización", None),
    (1, "1.3 Función económica de las R&W: la asimetría informativa", None),
    (1, "1.4 La carta de revelaciones (disclosure letter)", None),
    (0, "CAPÍTULO SEGUNDO. ORIGEN DE LAS R&W EN EL COMMON LAW", None),
    (1, "2.1 Naturaleza de las representations y de las warranties", None),
    (1, "2.2 El régimen de indemnización: cap, basket, de minimis y survival", None),
    (1, "2.3 Sandbagging y seguro de R&W (W&I insurance)", None),
    (1, "2.4 La lógica contractual anglosajona", None),
    (0, "CAPÍTULO TERCERO. EL PROBLEMA DE RECEPCIÓN EN EL DERECHO MEXICANO", "CAPÍTULO TERCERO"),
    (1, "3.1 El trasplante jurídico de figuras contractuales anglosajonas", "3.1 El trasplante"),
    (1, "3.2 La libertad contractual y sus límites", "3.2 La libertad"),
    (1, "3.3 El saneamiento por evicción", "3.3 El saneamiento por evicción"),
    (1, "3.4 El saneamiento por vicios ocultos", "3.4 El saneamiento por vicios"),
    (1, "3.5 Los vicios del consentimiento: error y dolo", "3.5 Los vicios"),
    (1, "3.6 Recapitulación y tránsito al problema de la naturaleza jurídica", "3.6 Recapitulación"),
    (0, "CAPÍTULO CUARTO. NATURALEZA JURÍDICA DE LAS R&W EN EL DERECHO MEXICANO", None),
    (0, "CAPÍTULO QUINTO. EL RÉGIMEN DE INDEMNIZACIÓN FRENTE AL CÓDIGO CIVIL", None),
    (0, "CAPÍTULO SEXTO. DERECHO COMPARADO", None),
    (0, "CAPÍTULO SÉPTIMO. CONCLUSIONES Y PROPUESTA", None),
    (0, "FUENTES DE CONSULTA", None),
]


# ---------- Decoración de página ----------
def _footer(canvas, doc):
    canvas.setFont("Times-Roman", 10)
    canvas.setFillColor(GRIS)
    canvas.drawCentredString(letter[0] / 2.0, 1.25 * cm, "\u2014  %d  \u2014" % doc.page)


def on_content_page(canvas, doc):
    canvas.saveState()
    y = letter[1] - 1.6 * cm
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(0.8)
    canvas.line(doc.leftMargin, y, letter[0] - doc.rightMargin, y)
    canvas.setFont("Times-Italic", 9)
    canvas.setFillColor(GRIS)
    canvas.drawCentredString(letter[0] / 2.0, y + 4, RUN_TITLE)
    _footer(canvas, doc)
    canvas.restoreState()


def on_prelim_page(canvas, doc):
    canvas.saveState()
    _footer(canvas, doc)
    canvas.restoreState()


def on_cover_page(canvas, doc):
    canvas.saveState()
    # marco exterior azul + filete interior dorado
    canvas.setStrokeColor(AZUL)
    canvas.setLineWidth(2)
    canvas.rect(1.5 * cm, 1.5 * cm, letter[0] - 3.0 * cm, letter[1] - 3.0 * cm)
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(0.8)
    canvas.rect(1.75 * cm, 1.75 * cm, letter[0] - 3.5 * cm, letter[1] - 3.5 * cm)
    canvas.restoreState()


# ---------- Secciones ----------
def cover_story():
    s = []
    unam = os.path.join(ASSETS, "unam.png")
    fes = os.path.join(ASSETS, "fes-aragon.png")
    uw, uh = 2.7 * cm, 2.7 * cm * (1236.0 / 1100.0)
    fw = fh = 2.5 * cm
    logo_tbl = Table([[Image(unam, width=uw, height=uh), "", Image(fes, width=fw, height=fh)]],
                     colWidths=[uw, (letter[0] - 4.6 * cm) - uw - fw, fw])
    logo_tbl.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                                  ("ALIGN", (0, 0), (0, 0), "LEFT"), ("ALIGN", (2, 0), (2, 0), "RIGHT")]))
    s += [Spacer(1, 0.35 * cm), logo_tbl, Spacer(1, 0.45 * cm)]
    s += [Paragraph("UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO", c_inst), Spacer(1, 0.12 * cm)]
    s += [Paragraph("FACULTAD DE ESTUDIOS SUPERIORES ARAGÓN", c_fac)]
    s += [rule(width="55%", sb=8, sa=8)]
    s += [Paragraph("LICENCIATURA EN DERECHO", c_sub), Spacer(1, 0.9 * cm)]
    titulo = ("NATURALEZA JURÍDICA Y RÉGIMEN DE RESPONSABILIDAD CONTRACTUAL DE LAS "
              "REPRESENTACIONES Y GARANTÍAS (<i>REPRESENTATIONS &amp; WARRANTIES</i>) Y DE "
              "LAS CLÁUSULAS DE INDEMNIZACIÓN (<i>CAP, BASKET, DE MINIMIS</i> Y "
              "<i>SURVIVAL</i>) EN LOS CONTRATOS DE COMPRAVENTA DE EMPRESAS "
              "(<i>SHARE PURCHASE AGREEMENTS</i>) BAJO EL DERECHO MEXICANO")
    s += [Paragraph(titulo, c_title), Spacer(1, 1.0 * cm)]
    s += [Paragraph("T  E  S  I  S", c_modb), Spacer(1, 0.18 * cm)]
    s += [Paragraph("QUE PARA OBTENER EL TÍTULO DE", c_mod)]
    s += [Paragraph("<b>LICENCIADO EN DERECHO</b>", c_mod), Spacer(1, 0.85 * cm)]
    s += [Paragraph("P  R  E  S  E  N  T  A", c_mod), Spacer(1, 0.12 * cm)]
    s += [Paragraph(NOMBRE_SUSTENTANTE, c_name)]
    s += [Spacer(1, 1.5 * cm), rule(width="45%", sb=2, sa=8)]
    s += [Paragraph("CIUDAD NEZAHUALCÓYOTL, ESTADO DE MÉXICO", c_sub)]
    return s


def agradecimientos_story():
    s = [Spacer(1, 1.2 * cm), Paragraph("AGRADECIMIENTOS", agra_title), rule()]
    for p in read_blocks(os.path.join(CONTENT, "agradecimientos.txt")):
        s.append(Paragraph(esc(p), agra))
    return s


def index_story(pages):
    s = [Paragraph("ÍNDICE", idx_title), rule()]
    rows = []
    for level, text, key in TOC:
        st = idx_l0 if level == 0 else idx_l1
        right = Paragraph(str(pages[key]), idx_pg) if (key and pages.get(key)) else Paragraph("En elaboración", idx_pend)
        rows.append([Paragraph(esc(text), st), right])
    usable = letter[0] - 3.0 * cm - 2.5 * cm
    t = Table(rows, colWidths=[usable - 2.6 * cm, 2.6 * cm])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                           ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    s.append(t)
    return s


def content_story():
    s = []
    s += heading("I. INTRODUCCIÓN")
    for p in read_blocks(os.path.join(CONTENT, "introduccion.txt")):
        s.append(Paragraph(esc(p), body))
    s.append(PageBreak())
    s += heading("II. PLANTEAMIENTO DEL PROBLEMA")
    pb = read_blocks(os.path.join(CONTENT, "planteamiento.txt"))
    for i, p in enumerate(pb):
        s.append(Paragraph(esc(p), research_q if i == len(pb) - 1 else body))
    s.append(PageBreak())
    # Apertura de capítulo
    s += [Spacer(1, 1.8 * cm),
          Paragraph("CAPÍTULO TERCERO", chap_num),
          rule(width="30%", sb=6, sa=10),
          Paragraph("EL PROBLEMA DE RECEPCIÓN DE LAS REPRESENTACIONES Y GARANTÍAS "
                    "EN EL DERECHO MEXICANO", chapsub)]
    for b in read_blocks(os.path.join(CONTENT, "capitulo3.txt")):
        if b.startswith("## "):
            s.append(Paragraph(esc(b[3:].strip()), subsec))
        elif b.startswith(">> "):
            s.append(quote_box(b[3:].strip()))
        else:
            s.append(Paragraph(esc(b), body))
    return s


def build(pages):
    doc = BaseDocTemplate(OUT, pagesize=letter, leftMargin=3.0 * cm, rightMargin=2.5 * cm,
                          topMargin=2.4 * cm, bottomMargin=2.2 * cm,
                          title="Naturaleza jurídica de las R&W y de la indemnización en el SPA (derecho mexicano)",
                          author="Tesis de Licenciatura en Derecho - FES Aragón, UNAM")
    cover_frame = Frame(2.2 * cm, 2.2 * cm, letter[0] - 4.4 * cm, letter[1] - 4.4 * cm, id="cover")
    content_frame = Frame(doc.leftMargin, doc.bottomMargin,
                          letter[0] - doc.leftMargin - doc.rightMargin,
                          letter[1] - doc.topMargin - doc.bottomMargin, id="content")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_frame], onPage=on_cover_page),
        PageTemplate(id="prelim", frames=[content_frame], onPage=on_prelim_page),
        PageTemplate(id="content", frames=[content_frame], onPage=on_content_page),
    ])
    story = cover_story()
    story += [NextPageTemplate("prelim"), PageBreak()]
    story += agradecimientos_story()
    story += [NextPageTemplate("content"), PageBreak()]
    story += index_story(pages)
    story += [PageBreak()]
    story += content_story()
    doc.build(story)


def detect_pages():
    import fitz
    d = fitz.open(OUT)
    start = 1
    for i in range(d.page_count):
        if d[i].search_for("ÍNDICE"):
            start = i + 1
    pages = {}
    for _, _, key in TOC:
        if not key:
            continue
        rng = range(1, d.page_count) if key == "AGRADECIMIENTOS" else range(start, d.page_count)
        for i in rng:
            if d[i].search_for(key):
                pages[key] = i + 1
                break
    d.close()
    return pages


if __name__ == "__main__":
    build({})
    pages = detect_pages()
    build(pages)
    print("PDF generado:", OUT)
    print("Páginas:", pages)
