"""CLI commands for service alerts."""

import json
import click

from ..cli_utils import get_client
from ..exceptions import InfobusError


@click.command("alerts")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json", "table"]),
    default="table",
    help="Output format",
)
@click.pass_context
def alerts_command(ctx, output_format: str):
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
                click.echo(
                    f"{'Alert ID':<15} {'Severity':<10} {'Header':<40} {'Created':<20}"
                )
                click.echo("-" * 85)
                for alert in alerts_data:
                    created_str = alert.created_at.strftime("%Y-%m-%d %H:%M:%S")
                    header_text = (
                        (alert.header_text[:37] + "...")
                        if len(alert.header_text) > 40
                        else alert.header_text
                    )
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
