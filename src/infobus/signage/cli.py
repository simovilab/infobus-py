import click
import yaml
import os
import sys
import json
from pathlib import Path

from .render import SignageRenderer
from .signage_models import Template


def cargar_plantilla(nombre_plantilla):
    """Carga una plantilla YAML desde la carpeta examples"""
    try:
        examples_dir = Path(__file__).parent / "examples"
        archivo_plantilla = examples_dir / f"{nombre_plantilla}.yaml"

        if not archivo_plantilla.exists():
            plantillas = [p.stem for p in examples_dir.glob("*.yaml")]
            click.echo(f"❌ No se encontró: '{nombre_plantilla}.yaml'")
            click.echo(f"📁 Disponibles: {', '.join(plantillas)}")
            return None

        with open(archivo_plantilla, "r", encoding="utf-8") as f:
            datos_yaml = yaml.safe_load(f)

        plantilla = Template(**datos_yaml)
        click.echo(f"✅ Plantilla '{nombre_plantilla}' cargada")
        return plantilla

    except Exception as e:
        click.echo(f"❌ Error cargando plantilla: {e}")
        return None


def generar_señal(template_name, output_format, output, data, dpi=300):
    """Función común para generar señales"""
    plantilla = cargar_plantilla(template_name)
    if not plantilla:
        return False

    try:
        renderizador = SignageRenderer()

        if output_format == "svg":
            resultado = renderizador.render_svg(plantilla, data)
            modo_archivo = "w"
        elif output_format == "png":
            resultado = renderizador.render_png(plantilla, data, dpi)
            modo_archivo = "wb"
        elif output_format == "pdf":
            resultado = renderizador.render_pdf(plantilla, data)
            modo_archivo = "wb"

        if output:
            with open(
                output,
                modo_archivo,
                encoding="utf-8" if output_format == "svg" else None,
            ) as f:
                f.write(resultado)
            click.echo(f"✅ Señal guardada en: {output}")
        else:
            nombre_default = f"señal_{template_name}.{output_format}"
            with open(
                nombre_default,
                modo_archivo,
                encoding="utf-8" if output_format == "svg" else None,
            ) as f:
                f.write(resultado)
            click.echo(f"📁 Señal guardada en: {nombre_default}")

        return True

    except Exception as e:
        click.echo(f"❌ Error generando señal: {e}")
        return False


@click.group()
def signage():
    """Generar señalética de transporte público"""
    pass


# COMANDO STOP
@signage.command()
@click.option(
    "--template",
    default="stop_vertical",
    help="Plantilla a usar (default: stop_vertical)",
)
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["svg", "png", "pdf"]),
    default="svg",
    help="Formato de salida (default: svg)",
)
@click.option("--size", help="Tamaño en formato WxH (ej: 300x450)(incompleto)")
@click.option("--dpi", default=300, help="DPI para PNG (default: 300)")
@click.option("--theme", help="Tema de colores (no implementado aún)")
@click.option("--lang", help="Idioma (no implementado aún)")
@click.option("--qr-url", help="URL para código QR")
@click.option("--output", "-o", help="Archivo de salida")
@click.option("--stop-name", required=True, help="Nombre de la parada (requerido)")
@click.option("--stop-code", required=True, help="Código de la parada (requerido)")
def stop(
    template,
    output_format,
    size,
    dpi,
    theme,
    lang,
    qr_url,
    output,
    stop_name,
    stop_code,
):
    """Generar señal para parada de autobús"""

    click.echo(f"🚏 Generando señal de parada...")

    datos = {"stop_name": stop_name, "stop_code": stop_code}

    if qr_url:
        datos["qr_url"] = qr_url
        click.echo(f"   🔲 QR URL: {qr_url}")

    click.echo(f"   📊 Datos: {datos}")

    if size:
        click.echo(f"   📏 Tamaño: {size} (opción ignorada por ahora)")
    if theme:
        click.echo(f"   🎨 Tema: {theme} (opción ignorada por ahora)")
    if lang:
        click.echo(f"   🌐 Idioma: {lang} (opción ignorada por ahora)")

    generar_señal(template, output_format, output, datos, dpi)


# COMANDO VEHICLE
@signage.command()
@click.option(
    "--template",
    default="vehicle_interior",
    help="Plantilla a usar (default: vehicle_interior)",
)
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["svg", "png", "pdf"]),
    default="svg",
    help="Formato de salida (default: svg)",
)
@click.option("--size", help="Tamaño en formato WxH (ej: 200x100)(incompleto)")
@click.option("--dpi", default=300, help="DPI para PNG (default: 300)")
@click.option("--theme", help="Tema de colores")
@click.option("--lang", help="Idioma")
@click.option("--qr-url", help="URL para código QR")
@click.option("--output", "-o", help="Archivo de salida")
@click.option("--route-number", required=True, help="Número de ruta (requerido)") 
@click.option("--destination", required=True, help="Destino (requerido)")

def vehicle(
    template,
    output_format,
    size,
    dpi,
    theme,
    lang,
    qr_url,
    output,
    route_number,
    destination,
):
    """Generar señal para vehículo"""

    click.echo(f"🚌 Generando señal para vehículo...")

    datos = {"route_number": route_number, "destination": destination}


    if qr_url:
        datos["qr_url"] = qr_url

    click.echo(f"   📊 Datos: {datos}")
    generar_señal(template, output_format, output, datos, dpi)


# COMANDO STATION
@signage.command()
@click.option(
    "--template",
    default="station_modular",
    help="Plantilla a usar (default: station_modular)",
)
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["svg", "png", "pdf"]),
    default="svg",
    help="Formato de salida (default: svg)",
)
@click.option("--size", help="Tamaño en formato WxH (incompleto)")
@click.option("--dpi", default=300, help="DPI para PNG")
@click.option("--theme", help="Tema de colores (no implementado aún)")
@click.option("--lang", help="Idioma" "(no implementado aún)")
@click.option("--qr-url", help="URL para código QR")
@click.option("--output", "-o", help="Archivo de salida")
@click.option("--station-name", required=True, help="Nombre de la estación (requerido)")
@click.option("--line-name", help="Nombre de la línea")
def station(
    template,
    output_format,
    size,
    dpi,
    theme,
    lang,
    qr_url,
    output,
    station_name,
    line_name,
):
    """Generar señal para estación"""

    click.echo(f"🏢 Generando señal para estación...")

    datos = {"station_name": station_name, "line_name": line_name or "Línea Principal"}

    if qr_url:
        datos["qr_url"] = qr_url

    click.echo(f"   📊 Datos: {datos}")
    generar_señal(template, output_format, output, datos, dpi)


# COMANDO ROUTE
@signage.command()
@click.option("--template", default="stop_vertical", help="Plantilla a usar")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["svg", "png", "pdf"]),
    default="svg",
    help="Formato de salida",
)
@click.option("--size", help="Tamaño en formato WxH (incompleto)")
@click.option("--dpi", default=300, help="DPI para PNG")
@click.option("--theme", help="Tema de colores")
@click.option("--lang", help="Idioma")
@click.option("--qr-url", help="URL para código QR")
@click.option("--output", "-o", help="Archivo de salida")
@click.option("--route-name", required=True, help="Nombre de la ruta (requerido)")
@click.option("--route-number", required=True, help="Número de ruta (requerido)")
def route(
    template,
    output_format,
    size,
    dpi,
    theme,
    lang,
    qr_url,
    output,
    route_name,
    route_number,
):
    """Generar señal de ruta"""

    click.echo(f"🛣️ Generando señal de ruta...")

    datos = {"route_name": route_name, "route_number": route_number}

    if qr_url:
        datos["qr_url"] = qr_url

    click.echo(f"   📊 Datos: {datos}")
    generar_señal(template, output_format, output, datos, dpi)


# COMANDO CUSTOM
@signage.command()
@click.option("--template", required=True, help="Plantilla a usar (requerido)")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["svg", "png", "pdf"]),
    default="svg",
    help="Formato de salida",
)
@click.option("--size", help="Tamaño en formato WxH (incompleto)")
@click.option("--dpi", default=300, help="DPI para PNG")
@click.option("--theme", help="Tema de colores")
@click.option("--lang", help="Idioma")
@click.option("--qr-url", help="URL para código QR")
@click.option("--output", "-o", help="Archivo de salida")
@click.option("--data", "-d", help='Datos en JSON (ej: \'{"campo1": "valor1"}\')')
def custom(template, output_format, size, dpi, theme, lang, qr_url, output, data):
    """Generar señal personalizada"""

    click.echo(f"🎨 Generando señal personalizada...")

    datos = {}
    if data:
        try:
            datos = json.loads(data)
        except json.JSONDecodeError as e:
            click.echo(f"❌ Error en JSON: {e}")
            return

    if qr_url:
        datos["qr_url"] = qr_url

    click.echo(f"   📊 Datos: {datos}")
    generar_señal(template, output_format, output, datos, dpi)


# COMANDO LIST 
@signage.command(name="list")
def list_templates():
    """Mostrar todas las plantillas disponibles"""
    examples_dir = Path(__file__).parent / "examples"
    plantillas = list(examples_dir.glob("*.yaml"))

    if not plantillas:
        click.echo("❌ No hay plantillas en 'examples/'")
        return

    click.echo("📁 Plantillas disponibles:")
    for plantilla in plantillas:
        with open(plantilla, "r", encoding="utf-8") as f:
            datos = yaml.safe_load(f)
            nombre = datos.get("name", plantilla.stem)
            desc = datos.get("description", "Sin descripción")
            click.echo(f"  • {plantilla.stem}")
            click.echo(f"    📝 {desc}")
            click.echo()


if __name__ == "__main__":
    signage()
