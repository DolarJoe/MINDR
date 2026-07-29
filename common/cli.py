# -*- coding: utf-8 -*-
"""CLI commands for MINDR."""

import click
from flask.cli import with_appcontext


@click.command("setup-oauth2-permissions")
@click.option(
    "--role",
    default="administration",
    help="Role name to grant permissions to (default: administration)",
)
@click.option("--user", default=None, help="User email to grant permissions to")
@with_appcontext
def setup_oauth2_permissions_cmd(role, user):
    """Grant OAuth2 client and token creation permissions.

    This command grants the necessary permissions for users/roles to create
    OAuth2 clients and generate API tokens with custom scopes.

    Example usage:

    \b
        # Grant to administration role (default)
        invenio db shell -c "from common.cli import setup_oauth2_permissions_cmd; setup_oauth2_permissions_cmd()"

        # Or run the script directly:
        python -m common.setup_oauth2_permissions

        # Grant to specific user
        python -m common.setup_oauth2_permissions --user user@example.com
    """
    from common.setup_oauth2_permissions import setup_oauth2_permissions

    setup_oauth2_permissions(role_name=role if not user else None, user_email=user)


def create_cli():
    """Create CLI blueprint."""
    cli = click.Group(name="mindr")
    cli.add_command(setup_oauth2_permissions_cmd)
    return cli
