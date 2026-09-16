from datetime import datetime
from html import escape
from pathlib import Path


class ReporteServicio:
    def __init__(self, ruta_logo=None):
        self.ruta_logo = Path(ruta_logo) if ruta_logo else None
        self.color_encabezado = "#1f2a44"
        self.color_resaltado = "#2563eb"
        self.color_borde = "#dbeafe"
        self.color_fila = "#f7fafc"

    def generar_reporte_ventas(self, ruta_salida, ventas, usuarios, libros):
        # ReportLab permite crear documentos PDF desde Python.
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_RIGHT
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import cm
        from reportlab.platypus import (
            Image,
            Paragraph,
            SimpleDocTemplate,
            Spacer,
            Table,
            TableStyle,
        )

        ruta_salida = Path(ruta_salida)
        ruta_salida.parent.mkdir(parents=True, exist_ok=True)

        estilos = getSampleStyleSheet()
        estilos.add(
            ParagraphStyle(
                name="TituloReporte",
                parent=estilos["Title"],
                textColor=colors.HexColor(self.color_encabezado),
                fontSize=18,
                leading=22,
                alignment=TA_RIGHT,
            )
        )
        estilos.add(
            ParagraphStyle(
                name="SubtituloReporte",
                parent=estilos["Normal"],
                textColor=colors.HexColor(self.color_resaltado),
                fontSize=11,
                alignment=TA_RIGHT,
            )
        )
        estilos.add(
            ParagraphStyle(
                name="CeldaTabla",
                parent=estilos["BodyText"],
                fontSize=8,
                leading=10,
            )
        )
        estilos.add(
            ParagraphStyle(
                name="NotaReporte",
                parent=estilos["BodyText"],
                textColor=colors.HexColor("#475569"),
                fontSize=9,
                leading=12,
            )
        )

        documento = SimpleDocTemplate(
            str(ruta_salida),
            pagesize=A4,
            rightMargin=1.5 * cm,
            leftMargin=1.5 * cm,
            topMargin=1.4 * cm,
            bottomMargin=1.4 * cm,
            title="Reporte de Ventas",
        )

        usuarios_por_id = {usuario.identificador: usuario for usuario in usuarios}
        libros_por_codigo = {libro.codigo: libro for libro in libros}
        elementos = []

        encabezado = self._crear_encabezado(Image, Paragraph, Table, TableStyle, estilos, colors)
        elementos.append(encabezado)
        elementos.append(Spacer(1, 14))

        fecha_generacion = datetime.now().strftime("%Y-%m-%d %H:%M")
        elementos.append(
            Paragraph(f"<b>Fecha de generacion:</b> {fecha_generacion}", estilos["BodyText"])
        )
        elementos.append(Spacer(1, 10))

        elementos.append(
            self._crear_tabla_resumen(
                Table,
                TableStyle,
                Paragraph,
                estilos,
                colors,
                ventas,
                usuarios_por_id,
                libros_por_codigo,
            )
        )
        elementos.append(Spacer(1, 16))
        elementos.append(Paragraph("Detalle de ventas registradas", estilos["Heading2"]))
        elementos.append(Spacer(1, 8))
        elementos.append(
            self._crear_tabla_ventas(
                Table,
                TableStyle,
                Paragraph,
                estilos,
                colors,
                ventas,
                usuarios_por_id,
                libros_por_codigo,
            )
        )
        elementos.append(Spacer(1, 14))
        elementos.append(
            Paragraph(
                "Documento generado automaticamente a partir de las ventas registradas "
                "en el sistema. Este reporte es pedagogico y no corresponde a un "
                "comprobante tributario.",
                estilos["NotaReporte"],
            )
        )

        documento.build(elementos)
        return str(ruta_salida)

    def _crear_encabezado(self, Image, Paragraph, Table, TableStyle, estilos, colors):
        logo = ""
        if self.ruta_logo and self.ruta_logo.exists():
            try:
                logo = Image(str(self.ruta_logo), width=2.4 * 28.35, height=2.4 * 28.35)
                logo.hAlign = "LEFT"
            except Exception:
                logo = ""

        titulo = [
            Paragraph("<b>Sistema Biblioteca</b>", estilos["TituloReporte"]),
            Paragraph("Reporte de Ventas", estilos["SubtituloReporte"]),
        ]
        tabla = Table([[logo, titulo]], colWidths=[5.2 * 28.35, 11.0 * 28.35])
        tabla.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#ffffff")),
                    ("LINEBELOW", (0, 0), (-1, -1), 1, colors.HexColor(self.color_borde)),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ]
            )
        )
        return tabla

    def _crear_tabla_resumen(
        self,
        Table,
        TableStyle,
        Paragraph,
        estilos,
        colors,
        ventas,
        usuarios_por_id,
        libros_por_codigo,
    ):
        usuarios_vendidos = {
            venta.usuario_id for venta in ventas if venta.usuario_id in usuarios_por_id
        }
        libros_vendidos = {
            venta.libro_codigo for venta in ventas if venta.libro_codigo in libros_por_codigo
        }
        datos = [
            ["Indicador", "Valor"],
            ["Ventas registradas", str(len(ventas))],
            ["Usuarios relacionados", str(len(usuarios_vendidos))],
            ["Libros diferentes vendidos", str(len(libros_vendidos))],
        ]
        tabla = Table(datos, colWidths=[8.0 * 28.35, 8.2 * 28.35])
        tabla.setStyle(self._estilo_tabla(TableStyle, colors))
        return tabla

    def _crear_tabla_ventas(
        self,
        Table,
        TableStyle,
        Paragraph,
        estilos,
        colors,
        ventas,
        usuarios_por_id,
        libros_por_codigo,
    ):
        datos = [["ID", "Fecha", "Usuario", "Libro", "Codigo"]]

        for venta in ventas:
            usuario = usuarios_por_id.get(venta.usuario_id)
            libro = libros_por_codigo.get(venta.libro_codigo)
            texto_usuario = (
                venta.usuario_id
                if usuario is None
                else f"{usuario.identificador} - {usuario.nombre}"
            )
            texto_libro = (
                venta.libro_codigo
                if libro is None
                else f"{libro.codigo} - {libro.titulo}"
            )
            datos.append(
                [
                    Paragraph(escape(venta.identificador), estilos["CeldaTabla"]),
                    Paragraph(escape(venta.fecha), estilos["CeldaTabla"]),
                    Paragraph(escape(texto_usuario), estilos["CeldaTabla"]),
                    Paragraph(escape(texto_libro), estilos["CeldaTabla"]),
                    Paragraph(escape(venta.libro_codigo), estilos["CeldaTabla"]),
                ]
            )

        tabla = Table(
            datos,
            colWidths=[2.0 * 28.35, 2.8 * 28.35, 4.1 * 28.35, 5.2 * 28.35, 2.1 * 28.35],
            repeatRows=1,
        )
        tabla.setStyle(self._estilo_tabla(TableStyle, colors))
        return tabla

    def _estilo_tabla(self, TableStyle, colors):
        return TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(self.color_encabezado)),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 9),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor(self.color_borde)),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor(self.color_fila)]),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
