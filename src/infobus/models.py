"""Infobús data models."""

from datetime import datetime
from typing import Optional, List, Any, Dict
from pydantic import BaseModel, Field, validator


class BaseInfobusModel(BaseModel):
    """Base model for all Infobús data objects."""
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True
        validate_assignment = True
        extra = "allow"  # Allow extra fields for API evolution


class Location(BaseInfobusModel):
    """Geographic location information."""
    
    latitude: float = Field(..., ge=-90, le=90, description="Latitude in decimal degrees")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude in decimal degrees")
    
    @validator('latitude', 'longitude')
    def validate_coordinates(cls, v):
        """Validate coordinate values are within valid ranges."""
        if not isinstance(v, (int, float)):
            raise ValueError('Coordinates must be numeric')
        return float(v)


class RealtimeData(BaseInfobusModel):
    """Real-time transit data."""
    
    id: str = Field(..., description="Unique identifier for this data point")
    route_id: str = Field(..., description="Route identifier")
    trip_id: Optional[str] = Field(None, description="Trip identifier")
    vehicle_id: Optional[str] = Field(None, description="Vehicle identifier")
    stop_id: Optional[str] = Field(None, description="Stop identifier")
    
    # Timing information
    timestamp: datetime = Field(..., description="Data timestamp")
    scheduled_arrival: Optional[datetime] = Field(None, description="Scheduled arrival time")
    estimated_arrival: Optional[datetime] = Field(None, description="Estimated arrival time")
    delay: Optional[int] = Field(None, description="Delay in seconds (positive = late)")
    
    # Position information
    location: Optional[Location] = Field(None, description="Current vehicle location")
    bearing: Optional[float] = Field(None, ge=0, le=360, description="Vehicle bearing in degrees")
    speed: Optional[float] = Field(None, ge=0, description="Vehicle speed")
    
    # Status information
    status: Optional[str] = Field(None, description="Current status")
    occupancy_status: Optional[str] = Field(None, description="Vehicle occupancy level")
    
    # Additional data
    extra_data: Optional[Dict[str, Any]] = Field(None, description="Additional data fields")


class Route(BaseInfobusModel):
    """Transit route information."""
    
    route_id: str = Field(..., description="Unique route identifier")
    agency_id: Optional[str] = Field(None, description="Agency that operates the route")
    route_short_name: Optional[str] = Field(None, description="Short name for the route")
    route_long_name: Optional[str] = Field(None, description="Full name for the route")
    route_desc: Optional[str] = Field(None, description="Description of the route")
    route_type: int = Field(..., description="GTFS route type")
    route_url: Optional[str] = Field(None, description="URL for route information")
    route_color: Optional[str] = Field(None, description="Route color (hex)")
    route_text_color: Optional[str] = Field(None, description="Route text color (hex)")
    
    # Operational information
    is_active: bool = Field(True, description="Whether the route is currently active")
    last_updated: Optional[datetime] = Field(None, description="Last update timestamp")
    
    @validator('route_color', 'route_text_color')
    def validate_hex_color(cls, v):
        """Validate hex color format."""
        if v is not None:
            if not v.startswith('#'):
                v = f"#{v}"
            if len(v) != 7 or not all(c in '0123456789ABCDEFabcdef' for c in v[1:]):
                raise ValueError('Invalid hex color format')
        return v


class Screen(BaseInfobusModel):
    """Display screen information."""
    
    screen_id: str = Field(..., description="Unique screen identifier")
    name: str = Field(..., description="Human-readable screen name")
    description: Optional[str] = Field(None, description="Screen description")
    
    # Location information
    location: Location = Field(..., description="Screen location")
    address: Optional[str] = Field(None, description="Physical address")
    
    # Hardware specifications
    size: Optional[str] = Field(None, description="Screen size")
    ratio: Optional[str] = Field(None, description="Screen aspect ratio")
    orientation: Optional[str] = Field(None, description="Screen orientation")
    has_sound: bool = Field(False, description="Whether screen has audio capability")
    
    # Operational information
    is_active: bool = Field(True, description="Whether the screen is currently active")
    last_seen: Optional[datetime] = Field(None, description="Last communication timestamp")
    firmware_version: Optional[str] = Field(None, description="Device firmware version")
    
    # Configuration
    refresh_interval: Optional[int] = Field(None, description="Data refresh interval in seconds")
    display_routes: Optional[List[str]] = Field(None, description="Route IDs to display")
    
    @validator('orientation')
    def validate_orientation(cls, v):
        """Validate screen orientation values."""
        if v is not None and v not in ['HORIZONTAL', 'VERTICAL']:
            raise ValueError('Orientation must be HORIZONTAL or VERTICAL')
        return v


class Alert(BaseInfobusModel):
    """Service alert information."""
    
    alert_id: str = Field(..., description="Unique alert identifier")
    cause: Optional[str] = Field(None, description="Cause of the alert")
    effect: Optional[str] = Field(None, description="Effect on service")
    
    # Text information
    header_text: str = Field(..., description="Alert header text")
    description_text: Optional[str] = Field(None, description="Detailed alert description")
    url: Optional[str] = Field(None, description="URL for more information")
    
    # Timing information
    active_period_start: Optional[datetime] = Field(None, description="Alert start time")
    active_period_end: Optional[datetime] = Field(None, description="Alert end time")
    created_at: datetime = Field(..., description="Alert creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    
    # Affected entities
    affected_routes: Optional[List[str]] = Field(None, description="Affected route IDs")
    affected_stops: Optional[List[str]] = Field(None, description="Affected stop IDs")
    affected_agencies: Optional[List[str]] = Field(None, description="Affected agency IDs")
    
    # Severity and priority
    severity_level: Optional[str] = Field(None, description="Alert severity level")
    priority: Optional[int] = Field(None, ge=1, le=5, description="Alert priority (1=highest)")
    
    @validator('severity_level')
    def validate_severity_level(cls, v):
        """Validate alert severity levels."""
        valid_levels = ['INFO', 'WARNING', 'SEVERE']
        if v is not None and v not in valid_levels:
            raise ValueError(f'Severity level must be one of: {valid_levels}')
        return v


class Weather(BaseInfobusModel):
    """Weather information for transit locations."""
    
    weather_id: str = Field(..., description="Unique weather data identifier")
    location: Location = Field(..., description="Weather observation location")
    
    # Timing
    observation_time: datetime = Field(..., description="Weather observation timestamp")
    
    # Weather conditions
    condition: str = Field(..., description="Weather condition description")
    temperature: float = Field(..., description="Temperature in degrees Celsius")
    humidity: Optional[float] = Field(None, ge=0, le=100, description="Relative humidity percentage")
    pressure: Optional[float] = Field(None, description="Atmospheric pressure in hPa")
    
    # Wind information
    wind_speed: Optional[float] = Field(None, ge=0, description="Wind speed in km/h")
    wind_direction: Optional[float] = Field(None, ge=0, le=360, description="Wind direction in degrees")
    
    # Precipitation
    precipitation: Optional[float] = Field(None, ge=0, description="Precipitation in mm")
    precipitation_probability: Optional[float] = Field(None, ge=0, le=100, description="Precipitation probability %")
    
    # Visibility
    visibility: Optional[float] = Field(None, ge=0, description="Visibility in kilometers")
    
    # UV and other indices
    uv_index: Optional[float] = Field(None, ge=0, description="UV index")


class ServiceStatus(BaseInfobusModel):
    """Service status information."""
    
    service_id: str = Field(..., description="Service identifier")
    status: str = Field(..., description="Current service status")
    last_updated: datetime = Field(..., description="Last status update")
    
    # Health metrics
    uptime_percentage: Optional[float] = Field(None, ge=0, le=100, description="Service uptime percentage")
    response_time: Optional[float] = Field(None, ge=0, description="Average response time in ms")
    error_rate: Optional[float] = Field(None, ge=0, le=100, description="Error rate percentage")
    
    # Additional information
    version: Optional[str] = Field(None, description="Service version")
    region: Optional[str] = Field(None, description="Service region")
    message: Optional[str] = Field(None, description="Additional status message")
    
    @validator('status')
    def validate_status(cls, v):
        """Validate service status values."""
        valid_statuses = ['OPERATIONAL', 'DEGRADED', 'PARTIAL_OUTAGE', 'MAJOR_OUTAGE', 'MAINTENANCE']
        if v not in valid_statuses:
            raise ValueError(f'Status must be one of: {valid_statuses}')
        return v
