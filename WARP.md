# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

**infobus-py** is a Python SDK and CLI toolkit for accessing Infobús external APIs and integrating transit data into research workflows. The project consists of two main components:

1. **API Client Library** (`src/infobus/`): A Python client for interacting with Infobús REST APIs
2. **Signage Generator** (`src/infobus/signage/`): A tool for generating transit signage (stops, vehicles, stations) in multiple formats

## Package Management

This project uses **uv** as the package manager (see `uv.lock`). The virtual environment is managed at `.venv/`.

## Development Commands

### Environment Setup

```bash
# Create/activate virtual environment
uv venv
source .venv/bin/activate  # macOS/Linux

# Install dependencies
uv pip install -e ".[dev]"
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=infobus

# Run specific test file
pytest tests/test_client.py

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Format and lint with ruff
ruff check src/ tests/
ruff format src/ tests/

# Type checking
mypy src/

# Note: No pre-commit hooks are configured yet
```

### Running CLIs

The CLI has a unified entry point with multiple subcommands:

```bash
# Main CLI help
infobus --help

# API commands (require --base-url and optional --token)
infobus api routes list --base-url https://example.com
infobus api routes get ROUTE_ID --base-url https://example.com

# Top-level API shortcuts (also require --base-url)
infobus realtime --base-url https://example.com
infobus screens --base-url https://example.com
infobus alerts --base-url https://example.com

# Signage commands (no API required)
infobus signage stop --stop-name "Main St" --stop-code "001"
infobus signage vehicle --route-number "5" --destination "Downtown"
infobus signage station --station-name "Central"
infobus signage list  # Show available templates

# Alternative: Run as module
python -m infobus --help
python -m infobus.signage.cli --help
```

### Single File/Module Testing

```bash
# Run a single test file
pytest tests/test_client.py

# Run specific test class or method
pytest tests/test_client.py::TestInfobusClient::test_client_initialization

# Run with specific marker (if configured)
pytest -m unit

# Test the signage module specifically
infobus signage --help
```

## Architecture

### Core Components

#### 1. API Client (`src/infobus/`)

**Structure:**
- `client.py`: `InfobusClient` class - main HTTP client with session management
- `models.py`: Pydantic models for API responses (RealtimeData, Route, Screen, Alert, Weather, etc.)
- `exceptions.py`: Custom exceptions (InfobusError, InfobusAPIError, InfobusConnectionError)
- `cli.py`: Main CLI entry point with modular command structure
- `cli_utils.py`: Shared utilities for CLI commands
- `realtime/cli.py`, `screens/cli.py`, `alerts/cli.py`: Modular CLI commands
- `api/cli.py`: API-specific CLI commands
- `__init__.py`: Package exports

**Key Patterns:**
- Uses `requests.Session` for connection pooling and header management
- Token-based authentication via `Authorization: Token <token>` header
- All API responses are parsed into Pydantic models for type safety
- Extra fields allowed in models (`extra = "allow"`) for API evolution
- CLI uses context passing pattern (`@click.pass_context`) for shared configuration
- Modular CLI structure: commands split into submodules (`realtime/`, `screens/`, `alerts/`, `api/`)
- Wrapper pattern used to inject API connection options into top-level commands

**API Client Design:**
- Base URL normalization (strips trailing slashes)
- Centralized error handling in `_make_request()` method
- Supports optional SSL verification and custom timeouts
- Environment variable support: `INFOBUS_BASE_URL`, `INFOBUS_TOKEN`, `INFOBUS_TIMEOUT`

#### 2. Signage Generator (`src/infobus/signage/`)

**Structure:**
- `signage_models.py`: Pydantic models for template definitions (Template, Dimensions, Grid, Font, Palette, FieldDef)
- `render.py`: `SignageRenderer` class - SVG/PNG/PDF rendering engine
- `cli.py`: Click-based CLI with subcommands (stop, vehicle, station, route, custom)
- `templates/`: Jinja2 templates (e.g., `base.svg.j2`)
- `examples/`: YAML template definitions (stop_vertical.yaml, vehicle_interior.yaml, station_modular.yaml)

**Key Patterns:**
- Template-driven design: YAML files define layout, fonts, colors, and fields
- Jinja2 templates render SVG from template + dynamic data
- QR code generation using `segno` library (embedded as base64 PNG in SVG)
- Multi-format output: SVG (native), PNG/PDF (via cairosvg conversion)
- Grid-based layout system with configurable rows/columns/margins

**Rendering Pipeline:**
1. Load YAML template → Pydantic `Template` model
2. Generate QR code (if `qr_url` provided) → base64 data URL
3. Render Jinja2 template with template config + dynamic data → SVG string
4. Convert SVG → PNG/PDF using cairosvg (with DPI/dimension handling)

**Template System:**
- Each template defines: dimensions, grid, fonts, palette, icons, required fields
- Position calculations vary by template type (stop vs vehicle vs station)
- Font families default to "Inter" but are configurable per template
- Unit conversion: supports both `px` and `mm` units

### Data Models

**Validation Patterns:**
- Coordinate validation: latitude (-90 to 90), longitude (-180 to 180)
- Hex color validation with automatic `#` prefix addition
- Enum-like validation for status fields (e.g., ServiceStatus, Alert severity)
- Optional fields use `Optional[T]` with `None` defaults
- `Field()` with descriptions for API documentation

**GTFS Alignment:**
- Route model follows GTFS route fields (route_id, route_type, colors, etc.)
- Compatible with GTFS Realtime specifications for transit data

## Import Patterns

**Main Client:**
```python
from infobus import InfobusClient
from infobus.exceptions import InfobusError, InfobusAPIError
```

**Signage:**
```python
from infobus.signage.signage_models import Template, Dimensions, Grid
from infobus.signage.render import SignageRenderer
```

**Note:** If you encounter import errors in tests, verify imports use `from infobus import InfobusClient` (not `from signage import`).

## Configuration

### API Client Configuration

Environment variables or CLI flags:
- `INFOBUS_BASE_URL`: Base URL of Infobús API instance
- `INFOBUS_TOKEN`: API authentication token
- `INFOBUS_TIMEOUT`: Request timeout (default: 30s)

Config file location (mentioned in README but not implemented): `~/.infobus/config.yaml`

### Signage Templates

Templates are YAML files in `src/infobus/signage/examples/`:
- `stop_vertical.yaml`: Bus stop signage
- `vehicle_interior.yaml`: Interior vehicle displays
- `station_modular.yaml`: Station/terminal signage

## Testing Strategy

**Current Coverage:**
- Basic client tests in `tests/test_client.py`
- Uses `unittest.mock` for mocking HTTP requests
- Tests cover: initialization, authentication, error handling, request flow

**Missing Tests:**
- No tests for CLI commands
- No tests for signage rendering
- No tests for Pydantic model validation
- No integration tests with real API

## Known Issues

1. **Entry point naming:** Only `infobus` command is defined in pyproject.toml; signage is accessed via `infobus signage` (not standalone `signage` command)
2. **Missing tool configuration:** No `[tool.ruff]`, `[tool.mypy]`, or `[tool.pytest]` sections in pyproject.toml
3. **Incomplete README examples:** README mentions features (pandas integration, geospatial support) not yet implemented
4. **CLI wrapper complexity:** Top-level commands use a wrapper pattern to inject API options, which adds complexity to command registration

## Dependencies

**Core:**
- `requests`: HTTP client
- `pydantic`: Data validation and models
- `click`: CLI framework
- `python-dateutil`: Date parsing

**Signage-specific:**
- `jinja2`: Template rendering
- `cairosvg`: SVG to PNG/PDF conversion
- `segno`: QR code generation

**Development:**
- `pytest`, `pytest-cov`: Testing
- `mypy`: Type checking
- `ruff`: Linting and formatting

## Related Projects

- [Infobús Server](https://github.com/fabianabarca/infobus): Main Django application
- [django-app-gtfs](https://github.com/fabianabarca/django-app-gtfs): GTFS data models for Django

## Code Style Notes

- **Language mixing:** Spanish function names and comments in signage CLI (`cargar_plantilla`, `generar_señal`, etc.) while main API client uses English throughout
- **Emoji usage:** Signage CLI output includes emojis (🚏, 🚌, ✅, ❌) for visual feedback
- **Click patterns:** Extensive use of help text and option documentation in all CLI commands
- **File organization:** Modular CLI structure with commands split into subdirectories by feature
