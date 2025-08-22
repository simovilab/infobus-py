"""Infobús Python Client Library.

A Python client library and CLI tools for accessing Infobús external APIs
and integrating transit data into research workflows.
"""

__version__ = "0.1.0"
__author__ = "Fabián Abarca"
__email__ = "ensinergia@gmail.com"
__license__ = "Apache-2.0"

# Import main client class for easy access
from .client import InfobusClient
from .exceptions import InfobusError, InfobusAPIError, InfobusConnectionError

__all__ = [
    "InfobusClient",
    "InfobusError",
    "InfobusAPIError", 
    "InfobusConnectionError",
]
