# -*- coding: utf-8 -*-
"""Genera el PDF académico (portada + Introducción + Planteamiento del Problema)."""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Image,
    NextPageTemplate, PageBreak, Table, TableStyle,
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase.pdfmetrics import stringWidth

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")
CONTENT = os.path.join(BASE, "content")
OUT = os.path.join(BASE, "Tesis_Introduccion_y_Planteamiento.pdf")

AZUL = colors.HexColor("#0A2342")

# ---------- Estilos ----------
body = ParagraphStyle(
    "body", fontName="Times-Roman", fontSize=12, leading=18,  # 1.5 aprox
    alignment=TA_JUSTIFY, firstLineIndent=1.25 * cm, spaceAfter=0,
)
section = ParagraphStyle(
    "section", fontName="Times-Bold", fontSize=14, leading=20,
    alignment=TA_CENTER, spaceBefore=6, spaceAfter=18, textColor=AZUL,
)
quote = ParagraphStyle(
    "quote", parent=body, fontName="Times-Italic", firstLineIndent=0,
    leftIndent=1.0 * cm, rightIndent=1.0 * cm,
)

# Estilos de portada
c_inst = ParagraphStyle("c_inst", fontName="Times-Bold", fontSize=14,
                        leading=18, alignment=TA_CENTER, textColor=AZUL)
c_fac = ParagraphStyle("c_fac", fontName="Times-Bold", fontSize=13,
                       leading=17, alignment=TA_CENTER, textColor=AZUL)
c_sub = ParagraphStyle("c_sub", fontName="Times-Roman", fontSize=12,
                       leading=16, alignment=TA_CENTER)
c_title = ParagraphStyle("c_title", fontName="Times-Bold", fontSize=14.5,
                         leading=20, alignment=TA_CENTER)
c_mod = ParagraphStyle("c_mod", fontName="Times-Roman", fontSize=12,
                       leading=18, alignment=TA_CENTER)
c_modb = ParagraphStyle("c_modb", fontName="Times-Bold", fontSize=12,
                        leading=18, alignment=TA_CENTER)


def read_paragraphs(path):
    with open(path, encoding="utf-8") as f:
        raw = f.read().strip()
    return [p.strip() for p in raw.split("\n\n") if p.strip()]


# ---------- Pies/encabezados ----------
def on_content_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Times-Roman", 10)
    canvas.setFillColor(colors.HexColor("#555555"))
    # línea superior
    canvas.setStrokeColor(colors.HexColor("#CCCCCC"))
    canvas.setLineWidth(0.5)
    canvas.line(doc.leftMargin, letter[1] - 1.7 * cm,
                letter[0] - doc.rightMargin, letter[1] - 1.7 * cm)
    canvas.drawString(doc.leftMargin, letter[1] - 1.55 * cm,
                      "Naturaleza jurídica de las R&W y de la indemnización en el SPA")
    # número de página
    canvas.drawCentredString(letter[0] / 2.0, 1.3 * cm, str(doc.page))
    canvas.restoreState()


def on_cover_page(canvas, doc):
    canvas.saveState()
    # marco decorativo
    canvas.setStrokeColor(AZUL)
    canvas.setLineWidth(2)
    canvas.rect(1.4 * cm, 1.4 * cm, letter[0] - 2.8 * cm, letter[1] - 2.8 * cm)
    canvas.setLineWidth(0.5)
    canvas.rect(1.65 * cm, 1.65 * cm, letter[0] - 3.3 * cm, letter[1] - 3.3 * cm)
    canvas.restoreState()


def build():
    doc = BaseDocTemplate(
        OUT, pagesize=letter,
        leftMargin=3.0 * cm, rightMargin=2.5 * cm,
        topMargin=2.2 * cm, bottomMargin=2.2 * cm,
        title="Naturaleza jurídica de las Representaciones y Garantías y de la indemnización en el SPA",
        author="Tesis de Licenciatura en Derecho - FES Aragón, UNAM",
    )

    cover_frame = Frame(2.2 * cm, 2.2 * cm, letter[0] - 4.4 * cm,
                        letter[1] - 4.4 * cm, id="cover")
    content_frame = Frame(doc.leftMargin, doc.bottomMargin,
                          letter[0] - doc.leftMargin - doc.rightMargin,
                          letter[1] - doc.topMargin - doc.bottomMargin,
                          id="content")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_frame], onPage=on_cover_page),
        PageTemplate(id="content", frames=[content_frame], onPage=on_content_page),
    ])

    story = []

    # ---------------- PORTADA ----------------
    unam = os.path.join(ASSETS, "unam.png")
    fes = os.path.join(ASSETS, "fes-aragon.png")
    uw, uh = 2.7 * cm, 2.7 * cm * (1236.0 / 1100.0)
    fw = fh = 2.5 * cm
    logo_tbl = Table(
        [[Image(unam, width=uw, height=uh), "", Image(fes, width=fw, height=fh)]],
        colWidths=[uw, (letter[0] - 4.4 * cm) - uw - fw, fw],
    )
    logo_tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (0, 0), "LEFT"),
        ("ALIGN", (2, 0), (2, 0), "RIGHT"),
    ]))
    story.append(Spacer(1, 0.3 * cm))
    story.append(logo_tbl)
    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph("UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO", c_inst))
    story.append(Spacer(1, 0.15 * cm))
    story.append(Paragraph("FACULTAD DE ESTUDIOS SUPERIORES ARAGÓN", c_fac))
    story.append(Spacer(1, 0.25 * cm))
    story.append(Paragraph("LICENCIATURA EN DERECHO", c_sub))
    story.append(Spacer(1, 1.0 * cm))

    titulo = ("NATURALEZA JURÍDICA Y RÉGIMEN DE RESPONSABILIDAD CONTRACTUAL DE LAS "
              "REPRESENTACIONES Y GARANTÍAS (<i>REPRESENTATIONS &amp; WARRANTIES</i>) Y DE "
              "LAS CLÁUSULAS DE INDEMNIZACIÓN (<i>CAP, BASKET, DE MINIMIS</i> Y "
              "<i>SURVIVAL</i>) EN LOS CONTRATOS DE COMPRAVENTA DE EMPRESAS "
              "(<i>SHARE PURCHASE AGREEMENTS</i>) BAJO EL DERECHO MEXICANO")
    story.append(Paragraph(titulo, c_title))
    story.append(Spacer(1, 1.0 * cm))

    story.append(Paragraph("T   E   S   I   S", c_modb))
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph("QUE PARA OBTENER EL TÍTULO DE:", c_mod))
    story.append(Paragraph("<b>LICENCIADO EN DERECHO</b>", c_mod))
    story.append(Spacer(1, 0.7 * cm))
    story.append(Paragraph("P   R   E   S   E   N   T   A   :", c_mod))
    story.append(Paragraph("<b>[ NOMBRE COMPLETO DEL SUSTENTANTE ]</b>", c_mod))
    story.append(Spacer(1, 0.7 * cm))
    story.append(Paragraph("ASESOR:", c_mod))
    story.append(Paragraph("<b>[ GRADO Y NOMBRE DEL ASESOR ]</b>", c_mod))
    story.append(Spacer(1, 1.2 * cm))
    story.append(Paragraph(
        "CIUDAD NEZAHUALCÓYOTL, ESTADO DE MÉXICO, 2026", c_sub))

    # ---------------- CONTENIDO ----------------
    story.append(NextPageTemplate("content"))
    story.append(PageBreak())

    story.append(Paragraph("I. INTRODUCCIÓN", section))
    for p in read_paragraphs(os.path.join(CONTENT, "introduccion.txt")):
        story.append(Paragraph(p, body))

    story.append(PageBreak())
    story.append(Paragraph("II. PLANTEAMIENTO DEL PROBLEMA", section))
    paras = read_paragraphs(os.path.join(CONTENT, "planteamiento.txt"))
    for i, p in enumerate(paras):
        if i == len(paras) - 1:
            # destacar la pregunta de investigación final
            story.append(Spacer(1, 0.2 * cm))
            story.append(Paragraph(p, quote))
        else:
            story.append(Paragraph(p, body))

    doc.build(story)
    print("PDF generado:", OUT)


if __name__ == "__main__":
    build()
