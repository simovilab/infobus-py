"""CLI commands for display screens."""

import json
import click

from ..cli_utils import get_client
from ..exceptions import InfobusError


@click.command("screens")
@click.option("--active-only", is_flag=True, help="Show only active screens")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json", "table"]),
    default="table",
    help="Output format",
)
@click.pass_context
def screens_command(ctx, active_only: bool, output_format: str):
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
                click.echo(
                    f"{'Screen ID':<15} {'Name':<20} {'Location':<25} {'Active':<6} {'Last Seen':<20}"
                )
                click.echo("-" * 86)
                for screen in screens_data:
                    location_str = f"{screen.location.latitude:.4f}, {screen.location.longitude:.4f}"
                    last_seen_str = (
                        screen.last_seen.strftime("%Y-%m-%d %H:%M:%S")
                        if screen.last_seen
                        else "N/A"
                    )
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
