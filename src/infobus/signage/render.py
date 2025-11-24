from jinja2 import Environment, FileSystemLoader
import cairosvg
import os
import tempfile
import segno
from io import BytesIO
import base64


class SignageRenderer:
    def __init__(self):
        template_path = os.path.join(os.path.dirname(__file__), "templates")
        self.env = Environment(loader=FileSystemLoader(template_path))

    def generar_qr_base64(self, url: str, size: int = 100) -> str:
        """Genera código QR y lo convierte a base64 para SVG"""
        try:
            # Crear código QR
            qr = segno.make(url)

            # Guardar en buffer como PNG
            buffer = BytesIO()
            qr.save(buffer, kind="png", scale=6, dark="#000000", light=None)

            # Convertir a base64
            qr_base64 = base64.b64encode(buffer.getvalue()).decode()
            return f"data:image/png;base64,{qr_base64}"

        except Exception as e:
            print(f"❌ Error generando QR: {e}")
            return ""

    def render_svg(self, template, data: dict) -> str:
        """Template + Data → SVG"""
        svg_template = self.env.get_template("base.svg.j2")

        # Generar QR si hay qr_url
        qr_code_base64 = ""

        # POSICIONES DE QR ESPECÍFICAS POR PLANTILLA
        qr_size = 300
        qr_margin = 20

        # Posiciones por defecto
        qr_x = template.dimensions.width
        qr_y = qr_margin

        # Posiciones específicas según el tipo de plantilla
        template_name = template.name.lower()

        if "stop" in template_name and "vertical" in template_name:
            qr_x = 225
            qr_y = template.dimensions.height

        elif "vehicle" in template_name and "interior" in template_name:
            qr_size = 150
            qr_x = 560
            qr_y = -150

        elif "station" in template_name and "modular" in template_name:
            qr_x = 1000
            qr_y = 600

        elif "route" in template_name:
            qr_x = qr_margin
            qr_y = template.dimensions.height - qr_size - qr_margin

        if data.get("qr_url"):
            qr_code_base64 = self.generar_qr_base64(data["qr_url"])
            print(f"   🔲 QR generado: {data['qr_url'][:30]}...")
            print(f"   📍 Posición QR: ({qr_x}, {qr_y}) - Tamaño: {qr_size}px")

        # Preparar parámetros para el template
        template_params = {
            # Dimensiones y GRID
            "width": template.dimensions.width,
            "height": template.dimensions.height,
            "unit": template.dimensions.unit,
            "grid": template.grid,
            # Colores
            "background_color": template.palette.background,
            "text_color": template.palette.text or "#000000",
            "icon_color": template.palette.icon_color
            or template.palette.text
            or "#000000",
            # QR
            "qr_code_base64": qr_code_base64,
            "qr_size": qr_size,
            "qr_x": qr_x,
            "qr_y": qr_y,
            # Íconos
            "icons": template.icons,
            # PASAMOS EL TEMPLATE COMPLETO para que Jinja2 lea las fuentes directamente
            "template": template,
            "data": data,
        }

        # Añadir todos los datos dinámicos (sin duplicados)
        template_params.update(data)

        return svg_template.render(**template_params)

    def render_png(self, template, data: dict, dpi: int = 300) -> bytes:
        """SVG → PNG"""
        # Generar SVG
        svg_content = self.render_svg(template, data)

        # Ajustar dimensiones según unidad'
        if template.dimensions.unit == "mm":
            # Convertir mm a píxeles (aproximadamente 3.78 px por mm)
            width_px = int(template.dimensions.width * 3.78)
            height_px = int(template.dimensions.height * 3.78)
        else:
            width_px = template.dimensions.width
            height_px = template.dimensions.height

        # Reemplazar dimensiones en el SVG para PNG
        svg_content_fixed = (
            svg_content.replace(
                f'width="{template.dimensions.width}{template.dimensions.unit}"',
                f'width="{width_px}"',
            )
            .replace(
                f'height="{template.dimensions.height}{template.dimensions.unit}"',
                f'height="{height_px}"',
            )
            .replace("pt", "px")
        )  # Convertir puntos a píxeles para mejor compatibilidad

        # Guardar temporalmente y convertir
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".svg", delete=False, encoding="utf-8"
        ) as f:
            f.write(svg_content_fixed)
            temp_file = f.name

        try:
            # Convertir desde archivo con dimensiones explícitas
            png_bytes = cairosvg.svg2png(
                url=temp_file, dpi=dpi, output_width=width_px, output_height=height_px
            )
            return png_bytes
        finally:
            # Limpiar
            os.unlink(temp_file)

    def render_pdf(self, template, data: dict) -> bytes:
        """SVG → PDF - VERSIÓN CORREGIDA PARA VEHICLE"""
        # Generar SVG
        svg_content = self.render_svg(template, data)

        template_name = template.name.lower()

        #  VEHICLE - PDF
        if "vehicle" in template_name:
            try:
                print("   🔄 Usando conversión directa para PDF vehicle...")
                return cairosvg.svg2pdf(bytestring=svg_content.encode("utf-8"))
            except Exception as e:
                print(f"   ⚠️  Error en conversión vehicle PDF: {e}")

                pass

        # Guardar temporalmente y convertir
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".svg", delete=False, encoding="utf-8"
        ) as f:
            f.write(svg_content)
            temp_file = f.name

        try:
            # Convertir desde archivo
            pdf_bytes = cairosvg.svg2pdf(url=temp_file)
            return pdf_bytes
        finally:
            os.unlink(temp_file)
