# Tesis · R&W e indemnización en el SPA bajo derecho mexicano

Documento académico (Licenciatura en Derecho, FES Aragón – UNAM).

**Tema:** Naturaleza jurídica y régimen de responsabilidad contractual de las *representations & warranties* y de las cláusulas de indemnización (*cap, basket, de minimis* y *survival*) en los contratos de compraventa de empresas (*Share Purchase Agreements*) bajo el derecho mexicano.

## Contenido del PDF (22 páginas)

- **Portada** institucional (escudo UNAM + emblema FES Aragón), con el nombre del sustentante (sin asesor, sin año).
- **Índice** con la estructura completa de la tesis (Introducción, Planteamiento, Capítulos I–VII y Fuentes); las secciones ya redactadas llevan número de página y las pendientes se marcan como *“En elaboración”*.
- **I. Introducción** (~4,140 palabras, prosa continua).
- **II. Planteamiento del Problema** (~2,260 palabras), cierra con la pregunta de investigación.
- **Capítulo Tercero — El problema de recepción en el derecho mexicano** (inicio), con **citas textuales** de artículos vigentes.

**Archivo principal:** [`Tesis_Introduccion_y_Planteamiento.pdf`](./Tesis_Introduccion_y_Planteamiento.pdf) · Times New Roman 12, interlineado ~1.5, márgenes académicos.

## Artículos citados textualmente (texto vigente verificado)

Verificados como *“Vigente, con las modificaciones”* en fuente legislativa mexicana en línea (leyes-mx.com), congruentes con el texto publicado en el **Diario Oficial de la Federación**:

**Código Civil Federal** (publicado en el DOF en cuatro partes: 26 de mayo, 14 de julio, 3 y 31 de agosto de 1928):
- Libertad/fuerza contractual y límites: arts. **1839, 1796, 8**.
- Saneamiento por evicción: arts. **2119, 2120, 2121**.
- Saneamiento por vicios ocultos: arts. **2142, 2143, 2144, 2149**.
- Vicios del consentimiento: arts. **1812, 1815, 1816**.
- Prescripción civil ordinaria: art. **1159**.

**Código de Comercio** (publicado en el DOF del 7 de octubre al 13 de diciembre de 1889; en vigor desde el 1 de enero de 1890):
- Autonomía de la voluntad mercantil: art. **78**.
- Supletoriedad del derecho civil: art. **81**.
- Prescripción mercantil ordinaria (diez años): art. **1047**.

## Estructura del repositorio

```
Tesis_Introduccion_y_Planteamiento.pdf   PDF final
build_pdf.py                             generador (ReportLab) con portada, índice y 2 pasadas para numerar
content/introduccion.txt                 Introducción
content/planteamiento.txt                Planteamiento del Problema
content/capitulo3.txt                    Capítulo 3 (inicio, con citas textuales)
assets/                                  logos (escudo UNAM, emblema FES Aragón)
```

## Regenerar el PDF

```bash
pip install reportlab cairosvg pymupdf
python3 build_pdf.py
```

> El nombre del sustentante se edita en la constante `NOMBRE_SUSTENTANTE` de `build_pdf.py`.

## Nota de verificación

El texto de los artículos se transcribió de una fuente que los marca como vigentes. Antes de la
entrega final conviene **cotejarlos contra el PDF oficial de la Cámara de Diputados / DOF**, pues
las reformas pueden modificar la redacción. La argumentación jurídica no inventa jurisprudencia ni
doctrina; las tesis del Semanario Judicial de la Federación, en su caso, deberán añadirse y
verificarse en los capítulos siguientes.
