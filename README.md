# Infobús Python Client

[![PyPI version](https://badge.fury.io/py/infobus.svg)](https://badge.fury.io/py/infobus)
[![Python Support](https://img.shields.io/pypi/pyversions/infobus.svg)](https://pypi.org/project/infobus/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

A Python client library and CLI tools for accessing Infobús external APIs and integrating transit data into research workflows.

## Overview

The `infobus` package provides a simple and efficient way to interact with Infobús APIs, enabling researchers and developers to:

- Access real-time transit data from public transportation systems
- Retrieve historical transit information for analysis
- Integrate GTFS Realtime feeds into research workflows
- Query screen and display information
- Access weather and alert data associated with transit stops

## Installation

```bash
# Install from PyPI (when available)
pip install infobus

# Install from source
pip install git+https://github.com/simovilab/infobus-py.git

# Development installation
git clone https://github.com/simovilab/infobus-py.git
cd infobus-py
pip install -e ".[dev]"
```

## Quick Start

### Python Library

```python
from infobus import InfobusClient

# Initialize client
client = InfobusClient(base_url="https://your-infobus-instance.com")

# Get real-time transit data
transit_data = client.get_realtime_data()

# Query specific routes
route_info = client.get_route(route_id="route_123")

# Get screen information
screens = client.get_screens()
```

### Command Line Interface

```bash
# Get help
infobus --help

# List available routes
infobus routes list

# Get real-time data for a specific route
infobus realtime --route-id route_123

# Export data to CSV
infobus export --format csv --output data.csv
```

## Features

### Core API Client
- **RESTful API Integration**: Clean interface to Infobús REST endpoints
- **Authentication Support**: Token-based authentication handling
- **Error Handling**: Comprehensive error handling with meaningful messages
- **Rate Limiting**: Built-in rate limiting and retry logic

### Data Models
- **Pydantic Models**: Type-safe data models for all API responses
- **GTFS Compatibility**: Models aligned with GTFS and GTFS Realtime specifications
- **Validation**: Automatic data validation and serialization

### CLI Tools
- **Interactive Commands**: Easy-to-use command-line interface
- **Data Export**: Export data in multiple formats (JSON, CSV, XML)
- **Batch Operations**: Process multiple requests efficiently
- **Configuration Management**: Store and manage API credentials

### Research Integration
- **Pandas Integration**: Easy conversion to pandas DataFrames
- **Time Series Support**: Built-in support for time-based analysis
- **Geospatial Data**: Integration with geospatial libraries

## Configuration

Create a configuration file at `~/.infobus/config.yaml`:

```yaml
api:
  base_url: "https://your-infobus-instance.com"
  token: "your-api-token"
  timeout: 30

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/simovilab/infobus-py.git
cd infobus-py

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=infobus

# Run specific test file
pytest tests/test_client.py
```

### Code Quality

```bash
# Format code
black src/ tests/
isort src/ tests/

# Type checking
mypy src/

# Run pre-commit checks
pre-commit run --all-files
```

## API Reference

### InfobusClient

The main client class for interacting with Infobús APIs.

```python
class InfobusClient:
    def __init__(self, base_url: str, token: str = None, timeout: int = 30)
    def get_realtime_data(self, **filters) -> List[RealtimeData]
    def get_routes(self) -> List[Route]
    def get_route(self, route_id: str) -> Route
    def get_screens(self) -> List[Screen]
    def get_alerts(self) -> List[Alert]
```

### Data Models

- `RealtimeData`: Real-time transit information
- `Route`: Transit route information
- `Screen`: Display screen information
- `Alert`: Service alerts and notifications
- `Weather`: Weather data for transit locations

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Support

- **Documentation**: [GitHub README](https://github.com/simovilab/infobus-py#readme)
- **Issues**: [GitHub Issues](https://github.com/simovilab/infobus-py/issues)
- **Discussions**: [GitHub Discussions](https://github.com/simovilab/infobus-py/discussions)

## Related Projects

- [Infobús Server](https://github.com/fabianabarca/infobus) - The main Infobús Django application
- [django-app-gtfs](https://github.com/fabianabarca/django-app-gtfs) - GTFS data models for Django
