# -*- coding: utf-8 -*-
"""Genera el PDF académico: portada + índice + Introducción + Planteamiento + Capítulo 3."""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib import colors
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Image,
    NextPageTemplate, PageBreak, Table, TableStyle,
)
from reportlab.lib.styles import ParagraphStyle

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")
CONTENT = os.path.join(BASE, "content")
OUT = os.path.join(BASE, "Tesis_Introduccion_y_Planteamiento.pdf")

AZUL = colors.HexColor("#0A2342")
GRIS = colors.HexColor("#888888")

# ---- DATOS DE PORTADA (editar aquí) ----
NOMBRE_SUSTENTANTE = "ELÍAS ALEJO"   # <-- confirmar nombre completo y apellidos

# ---------- Estilos de cuerpo ----------
body = ParagraphStyle("body", fontName="Times-Roman", fontSize=12, leading=18,
                      alignment=TA_JUSTIFY, firstLineIndent=1.25 * cm)
section = ParagraphStyle("section", fontName="Times-Bold", fontSize=14, leading=20,
                         alignment=TA_CENTER, spaceBefore=6, spaceAfter=10, textColor=AZUL)
chapsub = ParagraphStyle("chapsub", fontName="Times-Bold", fontSize=12, leading=16,
                         alignment=TA_CENTER, spaceAfter=18, textColor=colors.black)
subsec = ParagraphStyle("subsec", fontName="Times-Bold", fontSize=12, leading=16,
                        alignment=TA_LEFT, spaceBefore=14, spaceAfter=6, textColor=AZUL)
quote = ParagraphStyle("quote", parent=body, fontName="Times-Italic", firstLineIndent=0,
                       leftIndent=1.2 * cm, rightIndent=1.0 * cm, spaceBefore=6, spaceAfter=6,
                       leading=16)
research_q = ParagraphStyle("rq", parent=body, fontName="Times-Italic", firstLineIndent=0,
                            leftIndent=1.0 * cm, rightIndent=1.0 * cm)

# Portada
c_inst = ParagraphStyle("c_inst", fontName="Times-Bold", fontSize=14, leading=18,
                        alignment=TA_CENTER, textColor=AZUL)
c_fac = ParagraphStyle("c_fac", fontName="Times-Bold", fontSize=13, leading=17,
                       alignment=TA_CENTER, textColor=AZUL)
c_sub = ParagraphStyle("c_sub", fontName="Times-Roman", fontSize=12, leading=16, alignment=TA_CENTER)
c_title = ParagraphStyle("c_title", fontName="Times-Bold", fontSize=14.5, leading=20, alignment=TA_CENTER)
c_mod = ParagraphStyle("c_mod", fontName="Times-Roman", fontSize=12, leading=18, alignment=TA_CENTER)
c_modb = ParagraphStyle("c_modb", fontName="Times-Bold", fontSize=12, leading=18, alignment=TA_CENTER)

# Índice
idx_title = ParagraphStyle("idx_title", fontName="Times-Bold", fontSize=14, leading=20,
                           alignment=TA_CENTER, spaceAfter=16, textColor=AZUL)
idx_l0 = ParagraphStyle("idx_l0", fontName="Times-Bold", fontSize=11, leading=15, alignment=TA_LEFT)
idx_l1 = ParagraphStyle("idx_l1", fontName="Times-Roman", fontSize=11, leading=15,
                        alignment=TA_LEFT, leftIndent=0.8 * cm)
idx_pg = ParagraphStyle("idx_pg", fontName="Times-Roman", fontSize=11, leading=15, alignment=TA_RIGHT)
idx_pend = ParagraphStyle("idx_pend", fontName="Times-Italic", fontSize=9, leading=15,
                          alignment=TA_RIGHT, textColor=GRIS)


def esc(t):
    """Escapa caracteres reservados de XML para texto plano (sin markup)."""
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def read_blocks(path):
    with open(path, encoding="utf-8") as f:
        raw = f.read().strip()
    return [b.strip() for b in raw.split("\n\n") if b.strip()]


# Estructura del índice: (nivel, texto, clave_de_búsqueda | None)
TOC = [
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


def on_content_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Times-Roman", 10)
    canvas.setFillColor(colors.HexColor("#555555"))
    canvas.setStrokeColor(colors.HexColor("#CCCCCC"))
    canvas.setLineWidth(0.5)
    canvas.line(doc.leftMargin, letter[1] - 1.7 * cm, letter[0] - doc.rightMargin, letter[1] - 1.7 * cm)
    canvas.drawString(doc.leftMargin, letter[1] - 1.55 * cm,
                      "Naturaleza jurídica de las R&W y de la indemnización en el SPA")
    canvas.drawCentredString(letter[0] / 2.0, 1.3 * cm, str(doc.page))
    canvas.restoreState()


def on_cover_page(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(AZUL)
    canvas.setLineWidth(2)
    canvas.rect(1.4 * cm, 1.4 * cm, letter[0] - 2.8 * cm, letter[1] - 2.8 * cm)
    canvas.setLineWidth(0.5)
    canvas.rect(1.65 * cm, 1.65 * cm, letter[0] - 3.3 * cm, letter[1] - 3.3 * cm)
    canvas.restoreState()


def cover_story():
    s = []
    unam = os.path.join(ASSETS, "unam.png")
    fes = os.path.join(ASSETS, "fes-aragon.png")
    uw, uh = 2.7 * cm, 2.7 * cm * (1236.0 / 1100.0)
    fw = fh = 2.5 * cm
    logo_tbl = Table([[Image(unam, width=uw, height=uh), "", Image(fes, width=fw, height=fh)]],
                     colWidths=[uw, (letter[0] - 4.4 * cm) - uw - fw, fw])
    logo_tbl.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                                  ("ALIGN", (0, 0), (0, 0), "LEFT"), ("ALIGN", (2, 0), (2, 0), "RIGHT")]))
    s += [Spacer(1, 0.3 * cm), logo_tbl, Spacer(1, 0.5 * cm)]
    s += [Paragraph("UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO", c_inst), Spacer(1, 0.15 * cm)]
    s += [Paragraph("FACULTAD DE ESTUDIOS SUPERIORES ARAGÓN", c_fac), Spacer(1, 0.25 * cm)]
    s += [Paragraph("LICENCIATURA EN DERECHO", c_sub), Spacer(1, 1.0 * cm)]
    titulo = ("NATURALEZA JURÍDICA Y RÉGIMEN DE RESPONSABILIDAD CONTRACTUAL DE LAS "
              "REPRESENTACIONES Y GARANTÍAS (<i>REPRESENTATIONS &amp; WARRANTIES</i>) Y DE "
              "LAS CLÁUSULAS DE INDEMNIZACIÓN (<i>CAP, BASKET, DE MINIMIS</i> Y "
              "<i>SURVIVAL</i>) EN LOS CONTRATOS DE COMPRAVENTA DE EMPRESAS "
              "(<i>SHARE PURCHASE AGREEMENTS</i>) BAJO EL DERECHO MEXICANO")
    s += [Paragraph(titulo, c_title), Spacer(1, 1.1 * cm)]
    s += [Paragraph("T   E   S   I   S", c_modb), Spacer(1, 0.2 * cm)]
    s += [Paragraph("QUE PARA OBTENER EL TÍTULO DE:", c_mod)]
    s += [Paragraph("<b>LICENCIADO EN DERECHO</b>", c_mod), Spacer(1, 0.9 * cm)]
    s += [Paragraph("P   R   E   S   E   N   T   A   :", c_mod)]
    s += [Paragraph("<b>%s</b>" % NOMBRE_SUSTENTANTE, c_mod), Spacer(1, 1.6 * cm)]
    s += [Paragraph("CIUDAD NEZAHUALCÓYOTL, ESTADO DE MÉXICO", c_sub)]
    return s


def index_story(pages):
    s = [Paragraph("ÍNDICE", idx_title)]
    rows = []
    for level, text, key in TOC:
        st = idx_l0 if level == 0 else idx_l1
        if key and pages.get(key):
            right = Paragraph(str(pages[key]), idx_pg)
        else:
            right = Paragraph("En elaboración", idx_pend)
        rows.append([Paragraph(esc(text), st), right])
    usable = letter[0] - 3.0 * cm - 2.5 * cm
    t = Table(rows, colWidths=[usable - 2.6 * cm, 2.6 * cm])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 1),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
                           ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    s.append(t)
    return s


def content_story():
    s = [Paragraph("I. INTRODUCCIÓN", section)]
    for p in read_blocks(os.path.join(CONTENT, "introduccion.txt")):
        s.append(Paragraph(esc(p), body))
    s.append(PageBreak())
    s.append(Paragraph("II. PLANTEAMIENTO DEL PROBLEMA", section))
    pb = read_blocks(os.path.join(CONTENT, "planteamiento.txt"))
    for i, p in enumerate(pb):
        s.append(Paragraph(esc(p), research_q if i == len(pb) - 1 else body))
    s.append(PageBreak())
    s.append(Paragraph("CAPÍTULO TERCERO", section))
    s.append(Paragraph("EL PROBLEMA DE RECEPCIÓN DE LAS REPRESENTACIONES Y GARANTÍAS "
                       "EN EL DERECHO MEXICANO", chapsub))
    for b in read_blocks(os.path.join(CONTENT, "capitulo3.txt")):
        if b.startswith("## "):
            s.append(Paragraph(esc(b[3:].strip()), subsec))
        elif b.startswith(">> "):
            s.append(Paragraph(esc(b[3:].strip()), quote))
        else:
            s.append(Paragraph(esc(b), body))
    return s


def build(pages):
    doc = BaseDocTemplate(OUT, pagesize=letter, leftMargin=3.0 * cm, rightMargin=2.5 * cm,
                          topMargin=2.2 * cm, bottomMargin=2.2 * cm,
                          title="Naturaleza jurídica de las R&W y de la indemnización en el SPA (derecho mexicano)",
                          author="Tesis de Licenciatura en Derecho - FES Aragón, UNAM")
    cover_frame = Frame(2.2 * cm, 2.2 * cm, letter[0] - 4.4 * cm, letter[1] - 4.4 * cm, id="cover")
    content_frame = Frame(doc.leftMargin, doc.bottomMargin,
                          letter[0] - doc.leftMargin - doc.rightMargin,
                          letter[1] - doc.topMargin - doc.bottomMargin, id="content")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_frame], onPage=on_cover_page),
        PageTemplate(id="content", frames=[content_frame], onPage=on_content_page),
    ])
    story = cover_story()
    story += [NextPageTemplate("content"), PageBreak()]
    story += index_story(pages)
    story += [PageBreak()]
    story += content_story()
    doc.build(story)


def detect_pages():
    import fitz
    d = fitz.open(OUT)
    # localizar el final del índice para no confundir entradas del índice con el contenido
    start = 1
    for i in range(d.page_count):
        if d[i].search_for("ÍNDICE"):
            start = i + 1
    pages = {}
    for _, _, key in TOC:
        if not key:
            continue
        for i in range(start, d.page_count):
            if d[i].search_for(key):
                pages[key] = i + 1
                break
    d.close()
    return pages


if __name__ == "__main__":
    build({})              # 1a pasada (sin números) para medir
    pages = detect_pages()
    build(pages)           # 2a pasada con números reales
    print("PDF generado:", OUT)
    print("Páginas índice detectadas:", pages)
