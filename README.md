# Tesis · Introducción y Planteamiento del Problema

Documento académico (Licenciatura en Derecho, FES Aragón – UNAM) que contiene **únicamente**:

1. **Introducción** (~4,140 palabras, prosa continua, sin subtítulos ni listas).
2. **Planteamiento del Problema** (~2,260 palabras), que cierra con la pregunta de investigación.

**Tema:** Naturaleza jurídica y régimen de responsabilidad contractual de las *representations & warranties* y de las cláusulas de indemnización (*cap, basket, de minimis* y *survival*) en los contratos de compraventa de empresas (*Share Purchase Agreements*) bajo el derecho mexicano.

## Archivo principal

- **[`Tesis_Introduccion_y_Planteamiento.pdf`](./Tesis_Introduccion_y_Planteamiento.pdf)** — documento final con portada institucional (escudo UNAM + emblema FES Aragón), Times New Roman 12, interlineado ~1.5 y márgenes académicos.

## Estructura del repositorio

```
Tesis_Introduccion_y_Planteamiento.pdf   PDF final
build_pdf.py                             generador del PDF (ReportLab)
content/introduccion.txt                 texto de la Introducción
content/planteamiento.txt                texto del Planteamiento del Problema
assets/                                  logos (escudo UNAM, emblema FES Aragón)
```

## Regenerar el PDF

```bash
pip install reportlab cairosvg
python3 build_pdf.py
```

## Notas de verificación

El contenido jurídico se redactó **sin inventar** legislación, jurisprudencia ni doctrina. Las
referencias a artículos del derecho civil/mercantil mexicano (p. ej. libertad contractual,
saneamiento, vicios del consentimiento, orden público) se usan de forma conceptual y **deben
confirmarse contra el texto vigente** antes de la entrega final. Los campos de **sustentante** y
**asesor** en la portada son marcadores de posición a completar.

> Escudo de la UNAM: dominio público (Wikimedia Commons). Emblema de la FES Aragón: tomado del
> sitio institucional aragon.unam.mx; uso académico.
