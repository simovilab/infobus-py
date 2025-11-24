#!/bin/bash
# build_and_run.sh - Construye y ejecuta el contenedor Docker

echo "🐳 Construyendo contenedor Docker..."
docker build -t infobus-signage .

echo "🚀 Ejecutando comando..."
docker run --rm -v $(pwd)/output:/app/output infobus-signage ./run_signage.sh "$@"
