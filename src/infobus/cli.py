"""Command-line interface for Infobús client."""

import sys
import json
import csv
from pathlib import Path
from typing import Optional
import click
from datetime import datetime

from . import InfobusClient, __version__
from .exceptions import InfobusError


@click.group()
@click.version_option(version=__version__, prog_name="infobus")
@click.option(
    "--base-url",
    envvar="INFOBUS_BASE_URL",
    help="Base URL of the Infobús API instance"
)
@click.option(
    "--token",
    envvar="INFOBUS_TOKEN",
    help="API token for authentication"
)
@click.option(
    "--timeout",
    default=30,
    envvar="INFOBUS_TIMEOUT",
    help="Request timeout in seconds"
)
@click.option(
    "--verbose", "-v",
    is_flag=True,
    help="Enable verbose output"
)
@click.pass_context
def cli(ctx, base_url: str, token: str, timeout: int, verbose: bool):
    """Infobús API client command-line interface.
    
    Access real-time transit data from Infobús instances through the command line.
    """
    # Ensure context object exists
    ctx.ensure_object(dict)
    
    # Store configuration in context
    ctx.obj["base_url"] = base_url
    ctx.obj["token"] = token
    ctx.obj["timeout"] = timeout
    ctx.obj["verbose"] = verbose
    
    # Create client if base_url is provided
    if base_url:
        try:
            ctx.obj["client"] = InfobusClient(
                base_url=base_url,
                token=token,
                timeout=timeout
            )
        except Exception as e:
            if verbose:
                click.echo(f"Error creating client: {e}", err=True)
            ctx.obj["client"] = None
    else:
        ctx.obj["client"] = None


def get_client(ctx) -> InfobusClient:
    """Get the client from context, with error handling."""
    if not ctx.obj.get("client"):
        if not ctx.obj.get("base_url"):
            raise click.ClickException(
                "Base URL is required. Set with --base-url or INFOBUS_BASE_URL environment variable."
            )
        else:
            raise click.ClickException("Failed to create API client.")
    return ctx.obj["client"]


@cli.group()
@click.pass_context
def routes(ctx):
    """Commands for working with transit routes."""
    pass


@routes.command("list")
@click.option(
    "--format", "output_format",
    type=click.Choice(["json", "table", "csv"]),
    default="table",
    help="Output format"
)
@click.option(
    "--output", "-o",
    type=click.Path(),
    help="Output file (default: stdout)"
)
@click.pass_context
def list_routes(ctx, output_format: str, output: Optional[str]):
    """List all available routes."""
    try:
        client = get_client(ctx)
        routes_data = client.get_routes()
        
        if output_format == "json":
            data = [route.dict() for route in routes_data]
            output_data = json.dumps(data, indent=2, default=str)
        elif output_format == "csv":
            if not routes_data:
                output_data = ""
            else:
                import io
                buffer = io.StringIO()
                writer = csv.DictWriter(buffer, fieldnames=routes_data[0].dict().keys())
                writer.writeheader()
                for route in routes_data:
                    writer.writerow(route.dict())
                output_data = buffer.getvalue()
        else:  # table format
            if not routes_data:
                output_data = "No routes found."
            else:
                # Simple table format
                output_data = f"{'Route ID':<15} {'Short Name':<15} {'Long Name':<30} {'Type':<5} {'Active':<6}\n"
                output_data += "-" * 71 + "\n"
                for route in routes_data:
                    output_data += (
                        f"{route.route_id:<15} "
                        f"{route.route_short_name or 'N/A':<15} "
                        f"{(route.route_long_name or 'N/A')[:29]:<30} "
                        f"{route.route_type:<5} "
                        f"{'Yes' if route.is_active else 'No':<6}\n"
                    )
        
        if output:
            Path(output).write_text(output_data)
            click.echo(f"Output written to {output}")
        else:
            click.echo(output_data)
            
    except InfobusError as e:
        raise click.ClickException(f"API error: {e}")
    except Exception as e:
        if ctx.obj.get("verbose"):
            raise
        raise click.ClickException(f"Unexpected error: {e}")


@routes.command("get")
@click.argument("route_id")
@click.option(
    "--format", "output_format",
    type=click.Choice(["json", "yaml"]),
    default="json",
    help="Output format"
)
@click.pass_context
def get_route(ctx, route_id: str, output_format: str):
    """Get information for a specific route."""
    try:
        client = get_client(ctx)
        route = client.get_route(route_id)
        
        if output_format == "json":
            click.echo(json.dumps(route.dict(), indent=2, default=str))
        else:  # yaml format
            import yaml
            click.echo(yaml.dump(route.dict(), default_flow_style=False))
            
    except InfobusError as e:
        raise click.ClickException(f"API error: {e}")
    except Exception as e:
        if ctx.obj.get("verbose"):
            raise
        raise click.ClickException(f"Unexpected error: {e}")


@cli.command("realtime")
@click.option(
    "--route-id",
    help="Filter by route ID"
)
@click.option(
    "--stop-id",
    help="Filter by stop ID"
)
@click.option(
    "--format", "output_format",
    type=click.Choice(["json", "table", "csv"]),
    default="table",
    help="Output format"
)
@click.option(
    "--output", "-o",
    type=click.Path(),
    help="Output file (default: stdout)"
)
@click.pass_context
def get_realtime(ctx, route_id: Optional[str], stop_id: Optional[str], output_format: str, output: Optional[str]):
    """Get real-time transit data."""
    try:
        client = get_client(ctx)
        
        # Build filters
        filters = {}
        if route_id:
            filters["route_id"] = route_id
        if stop_id:
            filters["stop_id"] = stop_id
            
        realtime_data = client.get_realtime_data(**filters)
        
        if output_format == "json":
            data = [item.dict() for item in realtime_data]
            output_data = json.dumps(data, indent=2, default=str)
        elif output_format == "csv":
            if not realtime_data:
                output_data = ""
            else:
                import io
                buffer = io.StringIO()
                writer = csv.DictWriter(buffer, fieldnames=realtime_data[0].dict().keys())
                writer.writeheader()
                for item in realtime_data:
                    writer.writerow(item.dict())
                output_data = buffer.getvalue()
        else:  # table format
            if not realtime_data:
                output_data = "No real-time data found."
            else:
                output_data = f"{'Route':<10} {'Vehicle':<10} {'Stop':<10} {'Status':<15} {'Delay':<8} {'Timestamp':<20}\n"
                output_data += "-" * 73 + "\n"
                for item in realtime_data:
                    delay_str = f"{item.delay}s" if item.delay is not None else "N/A"
                    timestamp_str = item.timestamp.strftime("%Y-%m-%d %H:%M:%S") if item.timestamp else "N/A"
                    output_data += (
                        f"{item.route_id:<10} "
                        f"{item.vehicle_id or 'N/A':<10} "
                        f"{item.stop_id or 'N/A':<10} "
                        f"{item.status or 'N/A':<15} "
                        f"{delay_str:<8} "
                        f"{timestamp_str:<20}\n"
                    )
        
        if output:
            Path(output).write_text(output_data)
            click.echo(f"Output written to {output}")
        else:
            click.echo(output_data)
            
    except InfobusError as e:
        raise click.ClickException(f"API error: {e}")
    except Exception as e:
        if ctx.obj.get("verbose"):
            raise
        raise click.ClickException(f"Unexpected error: {e}")


@cli.command("screens")
@click.option(
    "--active-only",
    is_flag=True,
    help="Show only active screens"
)
@click.option(
    "--format", "output_format",
    type=click.Choice(["json", "table"]),
    default="table",
    help="Output format"
)
@click.pass_context
def list_screens(ctx, active_only: bool, output_format: str):
    """List display screens."""
    try:
        client = get_client(ctx)
        screens_data = client.get_screens()
        
        # Filter active screens if requested
        if active_only:
            screens_data = [screen for screen in screens_data if screen.is_active]
        
        if output_format == "json":
            data = [screen.dict() for screen in screens_data]
            click.echo(json.dumps(data, indent=2, default=str))
        else:  # table format
            if not screens_data:
                click.echo("No screens found.")
            else:
                click.echo(f"{'Screen ID':<15} {'Name':<20} {'Location':<25} {'Active':<6} {'Last Seen':<20}")
                click.echo("-" * 86)
                for screen in screens_data:
                    location_str = f"{screen.location.latitude:.4f}, {screen.location.longitude:.4f}"
                    last_seen_str = screen.last_seen.strftime("%Y-%m-%d %H:%M:%S") if screen.last_seen else "N/A"
                    click.echo(
                        f"{screen.screen_id:<15} "
                        f"{screen.name:<20} "
                        f"{location_str:<25} "
                        f"{'Yes' if screen.is_active else 'No':<6} "
                        f"{last_seen_str:<20}"
                    )
                    
    except InfobusError as e:
        raise click.ClickException(f"API error: {e}")
    except Exception as e:
        if ctx.obj.get("verbose"):
            raise
        raise click.ClickException(f"Unexpected error: {e}")


@cli.command("alerts")
@click.option(
    "--format", "output_format",
    type=click.Choice(["json", "table"]),
    default="table",
    help="Output format"
)
@click.pass_context
def list_alerts(ctx, output_format: str):
    """List current service alerts."""
    try:
        client = get_client(ctx)
        alerts_data = client.get_alerts()
        
        if output_format == "json":
            data = [alert.dict() for alert in alerts_data]
            click.echo(json.dumps(data, indent=2, default=str))
        else:  # table format
            if not alerts_data:
                click.echo("No active alerts.")
            else:
                click.echo(f"{'Alert ID':<15} {'Severity':<10} {'Header':<40} {'Created':<20}")
                click.echo("-" * 85)
                for alert in alerts_data:
                    created_str = alert.created_at.strftime("%Y-%m-%d %H:%M:%S")
                    header_text = (alert.header_text[:37] + "...") if len(alert.header_text) > 40 else alert.header_text
                    click.echo(
                        f"{alert.alert_id:<15} "
                        f"{alert.severity_level or 'N/A':<10} "
                        f"{header_text:<40} "
                        f"{created_str:<20}"
                    )
                    
    except InfobusError as e:
        raise click.ClickException(f"API error: {e}")
    except Exception as e:
        if ctx.obj.get("verbose"):
            raise
        raise click.ClickException(f"Unexpected error: {e}")


def main():
    """Entry point for the CLI."""
    try:
        cli()
    except KeyboardInterrupt:
        click.echo("\nInterrupted by user", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Fatal error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
