"""CLI commands for real-time transit data."""

import json
import csv
from pathlib import Path
from typing import Optional
import click

from ..cli_utils import get_client
from ..exceptions import InfobusError


@click.command("realtime")
@click.option("--route-id", help="Filter by route ID")
@click.option("--stop-id", help="Filter by stop ID")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json", "table", "csv"]),
    default="table",
    help="Output format",
)
@click.option("--output", "-o", type=click.Path(), help="Output file (default: stdout)")
@click.pass_context
def realtime_command(
    ctx,
    route_id: Optional[str],
    stop_id: Optional[str],
    output_format: str,
    output: Optional[str],
):
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
                writer = csv.DictWriter(
                    buffer, fieldnames=realtime_data[0].dict().keys()
                )
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
                    timestamp_str = (
                        item.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                        if item.timestamp
                        else "N/A"
                    )
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