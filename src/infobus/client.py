"""Infobús API Client."""

from typing import Dict, List, Optional, Union
import requests
from urllib.parse import urljoin

from .exceptions import InfobusAPIError, InfobusConnectionError
from .models import RealtimeData, Route, Screen, Alert


class InfobusClient:
    """Main client for interacting with Infobús APIs."""
    
    def __init__(
        self,
        base_url: str,
        token: Optional[str] = None,
        timeout: int = 30,
        verify_ssl: bool = True
    ) -> None:
        """Initialize the Infobús client.
        
        Args:
            base_url: Base URL of the Infobús API instance
            token: API token for authentication (optional)
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
        # Setup session with common headers
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "infobus-py/0.1.0",
            "Accept": "application/json",
            "Content-Type": "application/json",
        })
        
        if token:
            self.session.headers["Authorization"] = f"Token {token}"
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        json: Optional[Dict] = None
    ) -> Union[Dict, List]:
        """Make an HTTP request to the API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (without base URL)
            params: URL parameters
            json: JSON body data
            
        Returns:
            Parsed JSON response
            
        Raises:
            InfobusConnectionError: If connection fails
            InfobusAPIError: If API returns an error
        """
        url = urljoin(self.base_url + "/", endpoint.lstrip("/"))
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json,
                timeout=self.timeout,
                verify=self.verify_ssl
            )
            
            # Raise for HTTP error status codes
            if response.status_code >= 400:
                error_msg = f"API request failed with status {response.status_code}"
                try:
                    error_data = response.json()
                    if "detail" in error_data:
                        error_msg = error_data["detail"]
                    elif "error" in error_data:
                        error_msg = error_data["error"]
                except ValueError:
                    error_msg = response.text or error_msg
                
                raise InfobusAPIError(error_msg, status_code=response.status_code)
            
            return response.json()
            
        except requests.exceptions.ConnectionError as e:
            raise InfobusConnectionError(f"Connection failed: {e}")
        except requests.exceptions.Timeout as e:
            raise InfobusConnectionError(f"Request timeout: {e}")
        except requests.exceptions.RequestException as e:
            raise InfobusConnectionError(f"Request failed: {e}")
    
    def get_realtime_data(self, **filters) -> List[RealtimeData]:
        """Get real-time transit data.
        
        Args:
            **filters: Optional filters for the data
            
        Returns:
            List of real-time transit data
        """
        data = self._make_request("GET", "/api/realtime/", params=filters)
        return [RealtimeData(**item) for item in data]
    
    def get_routes(self) -> List[Route]:
        """Get all available routes.
        
        Returns:
            List of route information
        """
        data = self._make_request("GET", "/api/routes/")
        return [Route(**item) for item in data]
    
    def get_route(self, route_id: str) -> Route:
        """Get information for a specific route.
        
        Args:
            route_id: Unique identifier for the route
            
        Returns:
            Route information
        """
        data = self._make_request("GET", f"/api/routes/{route_id}/")
        return Route(**data)
    
    def get_screens(self) -> List[Screen]:
        """Get all available screens.
        
        Returns:
            List of screen information
        """
        data = self._make_request("GET", "/api/screens/")
        return [Screen(**item) for item in data]
    
    def get_screen(self, screen_id: str) -> Screen:
        """Get information for a specific screen.
        
        Args:
            screen_id: Unique identifier for the screen
            
        Returns:
            Screen information
        """
        data = self._make_request("GET", f"/api/screens/{screen_id}/")
        return Screen(**data)
    
    def get_alerts(self) -> List[Alert]:
        """Get current service alerts.
        
        Returns:
            List of active alerts
        """
        data = self._make_request("GET", "/api/alerts/")
        return [Alert(**item) for item in data]
