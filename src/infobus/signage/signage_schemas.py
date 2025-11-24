from signage_models import Template
import json


def export_json_schema():
    """Exporta el JSON Schema para validación de plantillas"""
    schema = Template.schema()

    # Titlo y descrpción del schema
    schema["title"] = "Signage Template Schema"
    schema["description"] = (
        "Schema para plantillas de señalizacion de transporte publico"
    )

    # Guardar archivo
    with open("signage_template_schema.json", "w") as f:
        json.dump(schema, f, indent=2)

    print("✅ JSON Schema exportado como: signage_template_schema.json")
    return schema


# Para probar directamente
if __name__ == "__main__":
    export_json_schema()
