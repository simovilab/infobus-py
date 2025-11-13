"""Command-line interface for Infobús client."""

import sys
import json
import csv
from pathlib import Path
from typing import Optional
import click
from datetime import datetime

from . import __version__
from .client import InfobusClient
from .exceptions import InfobusError
from .cli_utils import get_client

# Import modular CLI commands
from .realtime.cli import realtime_command
from .screens.cli import screens_command
from .alerts.cli import alerts_command
from .signage.cli import signage as signage_group


@click.group()
@click.version_option(version=__version__, prog_name="infobus")
def cli():
    """Infobús CLI - Transit data API client and signage generator.

    Available subcommands:
    - api: Access Infobús REST APIs for routes and data
    - signage: Generate transit signage (stops, vehicles, stations)
    - realtime: Get real-time transit data
    - screens: List display screens
    - alerts: List service alerts
    """
    pass


# Add signage subcommand group
cli.add_command(signage_group, name="signage")


@cli.group(name="api")
@click.option(
    "--base-url", envvar="INFOBUS_BASE_URL", help="Base URL of the Infobús API instance"
)
@click.option("--token", envvar="INFOBUS_TOKEN", help="API token for authentication")
@click.option(
    "--timeout", default=30, envvar="INFOBUS_TIMEOUT", help="Request timeout in seconds"
)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.pass_context
def api_group(ctx, base_url: str, token: str, timeout: int, verbose: bool):
    """API client commands for accessing Infobús REST APIs.

    Access transit routes and related data from Infobús instances.
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
                base_url=base_url, token=token, timeout=timeout
            )
        except Exception as e:
            if verbose:
                click.echo(f"Error creating client: {e}", err=True)
            ctx.obj["client"] = None
    else:
        ctx.obj["client"] = None


# Add top-level commands with API context
for cmd in [realtime_command, screens_command, alerts_command]:
    # Wrap each command with API options
    cmd = click.option(
        "--base-url",
        envvar="INFOBUS_BASE_URL",
        help="Base URL of the Infobús API instance",
    )(cmd)
    cmd = click.option(
        "--token", envvar="INFOBUS_TOKEN", help="API token for authentication"
    )(cmd)
    cmd = click.option(
        "--timeout",
        default=30,
        envvar="INFOBUS_TIMEOUT",
        help="Request timeout in seconds",
    )(cmd)
    cmd = click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")(
        cmd
    )

    # Add a callback to setup API context
    original_callback = cmd.callback

    def make_wrapper(orig_callback):
        @click.pass_context
        def wrapper(ctx, *args, **kwargs):
            # Extract API options
            base_url = kwargs.pop("base_url", None)
            token = kwargs.pop("token", None)
            timeout = kwargs.pop("timeout", 30)
            verbose = kwargs.pop("verbose", False)

            # Setup context
            ctx.ensure_object(dict)
            ctx.obj["base_url"] = base_url
            ctx.obj["token"] = token
            ctx.obj["timeout"] = timeout
            ctx.obj["verbose"] = verbose

            if base_url:
                try:
                    ctx.obj["client"] = InfobusClient(
                        base_url=base_url, token=token, timeout=timeout
                    )
                except Exception as e:
                    if verbose:
                        click.echo(f"Error creating client: {e}", err=True)
                    ctx.obj["client"] = None
            else:
                ctx.obj["client"] = None

            # Call original
            return ctx.invoke(orig_callback, *args, **kwargs)

        wrapper.__name__ = orig_callback.__name__
        return wrapper

    cmd.callback = make_wrapper(original_callback)
    cli.add_command(cmd)


@api_group.group(name="routes")
@click.pass_context
def routes(ctx):
    """Commands for working with transit routes."""
    pass


@routes.command("list")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json", "table", "csv"]),
    default="table",
    help="Output format",
)
@click.option("--output", "-o", type=click.Path(), help="Output file (default: stdout)")
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
    "--format",
    "output_format",
    type=click.Choice(["json", "yaml"]),
    default="json",
    help="Output format",
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
