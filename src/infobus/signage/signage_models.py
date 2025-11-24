from pydantic import BaseModel, Field
from typing import Dict, List, Optional


class Dimensions(BaseModel):
    width: int  # Ancho en píxeles o milímetros
    height: int  # Alto en píxeles o milímetros
    unit: str = Field(
        default="px", description="Unidad de medida: px o mm"
    )  # Unidad de medida: px o mm


class Grid(BaseModel):
    rows: int = Field(
        ..., description="Numero de filas de la grid"
    )  # Número de filas de la grid
    cols: int = Field(
        ..., description="Numero de columnas de la grid"
    )  # Número de columnas de la grid
    margin: int = Field(5, description="Margen en pixeles")  # Margen en píxeles


class Font(BaseModel):
    family: str = Field(
        default="Inter", description="Familia tipografica"
    )  # Familia tipográfica
    size: int = Field(
        ..., description="Tamaño de fuente en puntos"
    )  # Tamaño de fuente en puntos
    weight: str = Field(
        default="400", description="Peso de la fuente (400=normal, 700=bold)"
    )  # Peso de la fuente (400=normal, 700=bold)


class Palette(BaseModel):
    background: str = Field("#FFFFFF", description="Color de fondo")
    secondary: Optional[str] = Field(None, description="Color secundario")
    text: Optional[str] = Field(None, description="Color del texto")
    icon_color: Optional[str] = Field(None, description="Color de íconos")


class FieldDef(BaseModel):
    name: str = Field(
        ..., description="Nombre identificador del campo"
    )  # Nombre identificador del campo
    type: str = Field(
        ..., description="Tipo: text, code, qr, icon"
    )  # Tipo: text, code, qr, icon
    required: bool = Field(
        default=True, description="Si el campo es obligatorio"
    )  # Si el campo es obligatorio


class Template(BaseModel):
    name: str = Field(
        ..., description="Nombre de la plantilla"
    )  # Nombre de la plantilla
    dimensions: Dimensions  # Dimensiones de la plantilla
    grid: Grid  # Configuración de la grid
    fonts: Dict[str, Font] = Field(
        ..., description="Diccionario de configuraciones de fuentes"
    )  # Diccionario de configuraciones de fuentes
    palette: Palette  # Paleta de colores
    icons: Dict[str, str] = Field(
        default_factory=dict, description="Diccionario de iconos disponibles"
    )  # Diccionario de íconos disponibles
    fields: List[FieldDef] = Field(
        ..., description="Lista de campos dinamicos"
    )  # Lista de campos dinámicos
