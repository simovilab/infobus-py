"""Shared utilities for CLI commands."""

import click
from .client import InfobusClient


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
