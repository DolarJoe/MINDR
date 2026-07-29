# -*- coding: utf-8 -*-
"""Script to grant OAuth2 permissions to users and roles.

This script must be run within the Flask application context using invenio shell.

Usage:
    # Grant to administration role (default)
    $ invenio shell << EOF
    from common.setup_oauth2_permissions import setup_oauth2_permissions
    setup_oauth2_permissions()
    EOF

    # Grant to specific user
    $ invenio shell << EOF
    from common.setup_oauth2_permissions import setup_oauth2_permissions
    setup_oauth2_permissions(user_email='user@example.com')
    EOF

    # Or create a Python script:
    $ cat > /tmp/setup_oauth.py << 'SCRIPT'
    from common.setup_oauth2_permissions import setup_oauth2_permissions
    setup_oauth2_permissions()
    SCRIPT
    $ invenio shell < /tmp/setup_oauth.py
"""

from click import secho
from invenio_access import action_factory
from invenio_access.models import ActionRoles, ActionUsers
from invenio_accounts.models import Role, User
from invenio_db import db


def setup_oauth2_permissions(role_name="administration", user_email=None):
    """Grant OAuth2 client and token creation permissions.

    Args:
        role_name: Name of the role to grant permissions to (default: "administration")
        user_email: Email of a specific user to grant permissions to (optional)
    """
    actions_to_grant = [
        "oauth2server-client-create",
        "oauth2server-token-create",
        "oauth2server-tokens-generate",
    ]

    # Grant permissions to role
    if role_name:
        secho(f"Granting OAuth2 permissions to role '{role_name}'...", fg="green")
        admin_role = Role.query.filter_by(name=role_name).first()

        if not admin_role:
            secho(f"Role '{role_name}' not found. Creating it...", fg="yellow")
            admin_role = Role(name=role_name)
            db.session.add(admin_role)
            db.session.flush()

        for action_name in actions_to_grant:
            action = action_factory(action_name)
            existing = ActionRoles.query.filter_by(
                action=action_name, role_id=admin_role.id
            ).first()

            if existing:
                secho(f"  ✓ {action_name} already granted to {role_name}", fg="cyan")
            else:
                db.session.add(ActionRoles.allow(action, role=admin_role))
                secho(f"  ✓ Granted {action_name} to {role_name}", fg="green")

    # Grant permissions to specific user
    if user_email:
        secho(f"\nGranting OAuth2 permissions to user '{user_email}'...", fg="green")
        user = User.query.filter_by(email=user_email).first()

        if not user:
            secho(f"User '{user_email}' not found.", fg="red")
            return

        for action_name in actions_to_grant:
            action = action_factory(action_name)
            existing = ActionUsers.query.filter_by(
                action=action_name, user_id=user.id
            ).first()

            if existing:
                secho(f"  ✓ {action_name} already granted to {user_email}", fg="cyan")
            else:
                db.session.add(ActionUsers.allow(action, user=user))
                secho(f"  ✓ Granted {action_name} to {user_email}", fg="green")

    # Commit all changes
    db.session.commit()
    secho("\n✓ OAuth2 permissions setup completed successfully!", fg="green")

    # Verify scopes are available
    from flask import current_app

    oauth2_ext = current_app.extensions.get("invenio-oauth2server")
    if oauth2_ext:
        secho("\nAvailable custom scopes:", fg="yellow")
        for scope_id, scope_obj in oauth2_ext.scopes.items():
            is_internal = getattr(scope_obj, "is_internal", False)
            if not is_internal and scope_id.startswith("rdm:"):
                secho(f"  • {scope_id}: {scope_obj.help_text}", fg="cyan")


if __name__ == "__main__":
    print(__doc__)
    print("\nNote: This script must be run within 'invenio shell' context.")
    print("See the usage examples above.")
