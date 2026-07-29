# -*- coding: utf-8 -*-
"""Custom OAuth2 scopes for MINDR."""

from invenio_oauth2server.models import Scope

# Full access scope for API tokens
rdm_full_access = Scope(id_="rdm:full-access", help_text="Allow full read-write access to records and data via API", group="rdm")

# Read-only scope for records
rdm_read = Scope(id_="rdm:read", help_text="Allow read-only access to records via API", group="rdm")

# Write scope for records
rdm_write = Scope(id_="rdm:write", help_text="Allow create and update access to records via API", group="rdm")
