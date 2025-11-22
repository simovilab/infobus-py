FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    libcairo2-dev \
    libpango1.0-dev \
    fonts-inter \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PIP_ROOT_USER_ACTION=ignore

# Instalar uv y configurar PATH correctamente
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

COPY pyproject.toml .
COPY README.md .
COPY src/ ./src/
COPY run_signage.sh .

RUN uv venv
RUN uv sync
RUN chmod +x run_signage.sh

# CAMBIO CLAVE: Crear directorio output y cambiar WORKDIR
RUN mkdir -p /app/output
WORKDIR /app/output

# El ENTRYPOINT debe apuntar al script en /app
ENTRYPOINT ["/app/run_signage.sh"]