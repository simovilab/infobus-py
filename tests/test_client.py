"""Basic tests for Infobús client."""

import pytest
from unittest.mock import Mock, patch
from infobus import InfobusClient
from infobus.exceptions import InfobusAPIError, InfobusConnectionError


class TestInfobusClient:
    """Test cases for InfobusClient."""
    
    def test_client_initialization(self):
        """Test client initialization with default parameters."""
        client = InfobusClient(base_url="https://api.example.com")
        assert client.base_url == "https://api.example.com"
        assert client.token is None
        assert client.timeout == 30
        assert client.verify_ssl is True
    
    def test_client_initialization_with_token(self):
        """Test client initialization with authentication token."""
        client = InfobusClient(
            base_url="https://api.example.com",
            token="test-token"
        )
        assert client.token == "test-token"
        assert "Authorization" in client.session.headers
        assert client.session.headers["Authorization"] == "Token test-token"
    
    def test_client_base_url_normalization(self):
        """Test that trailing slashes are removed from base URL."""
        client = InfobusClient(base_url="https://api.example.com/")
        assert client.base_url == "https://api.example.com"
    
    @patch('infobus.client.requests.Session.request')
    def test_successful_api_request(self, mock_request):
        """Test successful API request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "test"}
        mock_request.return_value = mock_response
        
        client = InfobusClient(base_url="https://api.example.com")
        result = client._make_request("GET", "/test")
        
        assert result == {"data": "test"}
        mock_request.assert_called_once()
    
    @patch('infobus.client.requests.Session.request')
    def test_api_error_handling(self, mock_request):
        """Test API error response handling."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"detail": "Not found"}
        mock_request.return_value = mock_response
        
        client = InfobusClient(base_url="https://api.example.com")
        
        with pytest.raises(InfobusAPIError) as exc_info:
            client._make_request("GET", "/test")
        
        assert exc_info.value.status_code == 404
        assert "Not found" in str(exc_info.value)
    
    @patch('infobus.client.requests.Session.request')
    def test_connection_error_handling(self, mock_request):
        """Test connection error handling."""
        import requests
        mock_request.side_effect = requests.exceptions.ConnectionError("Connection failed")
        
        client = InfobusClient(base_url="https://api.example.com")
        
        with pytest.raises(InfobusConnectionError) as exc_info:
            client._make_request("GET", "/test")
        
        assert "Connection failed" in str(exc_info.value)
    
    def test_user_agent_header(self):
        """Test that User-Agent header is set correctly."""
        client = InfobusClient(base_url="https://api.example.com")
        assert "User-Agent" in client.session.headers
        assert "infobus-py" in client.session.headers["User-Agent"]


if __name__ == "__main__":
    pytest.main([__file__])
