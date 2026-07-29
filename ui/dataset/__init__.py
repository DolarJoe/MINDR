from oarepo_ui.resources import BabelComponent
from oarepo_ui.resources.components import (
    # AllowedCommunitiesComponent,
    AllowedHtmlTagsComponent,
    EmptyRecordAccessComponent,
    FilesComponent,
    FilesLockedComponent,
    FilesQuotaAndTransferComponent,
    RecordRestrictionComponent,
    PermissionsComponent,
)
from oarepo_ui.resources.components.base import UIResourceComponent
from oarepo_ui.resources.components.custom_fields import CustomFieldsComponent
from oarepo_ui.resources.records.config import RecordsUIResourceConfig
from oarepo_ui.resources.records.resource import RecordsUIResource
from oarepo_ui.utils import can_view_deposit_page
from flask_menu import current_menu
from invenio_i18n import lazy_gettext as _
from oarepo_ui.overrides import UIComponent
from oarepo_ui.overrides.components import UIComponentImportMode
from oarepo_ui.proxies import current_oarepo_ui
from oarepo_rdm.ui.components import (
    CommunitiesMembershipsComponent,
    RDMVocabularyOptionsComponent,
)

class FilesEnabledEmptyRecordComponent(UIResourceComponent):
    """Enable files by default on the empty deposit record.

    The dataset model's empty record (built via ``dump_empty``) ships with
    ``files.enabled`` set to ``None``. Invenio RDM's deposit record serializer
    (:py:meth:`RDMDepositRecordSerializer._removeEmptyValues`) drops every key
    whose value is empty/null, so the whole ``files`` object is stripped from
    the formik initial values. The deposit ``AccessRightField`` then crashes
    with ``TypeError: ... values.files is undefined`` when reading
    ``formik.form.values.files.enabled``.

    Setting ``enabled`` to ``True`` (a boolean, which the serializer keeps)
    ensures ``files`` survives into the formik values and matches the standard
    Invenio RDM behaviour where a new draft has files enabled.
    """

    def empty_record(self, *, empty_data, **kwargs):
        """Ensure the empty record advertises files as enabled."""
        empty_data.setdefault("files", {})
        empty_data["files"]["enabled"] = True


class DatasetUIResourceConfig(RecordsUIResourceConfig):
    template_folder = "templates"
    url_prefix = "/dataset"
    blueprint_name = "dataset_ui"
    model_name = "dataset"

    search_component = UIComponent(
        "DatasetResultsListItem",
        "@js/dataset/search/ResultsListItem",
        UIComponentImportMode.DEFAULT
    )

    components = [
        AllowedHtmlTagsComponent,
        BabelComponent,
        PermissionsComponent,
        FilesComponent,
        # AllowedCommunitiesComponent,
        CustomFieldsComponent,
        RecordRestrictionComponent,
        EmptyRecordAccessComponent,
        FilesEnabledEmptyRecordComponent,
        FilesLockedComponent,
        FilesQuotaAndTransferComponent,
    ]

    try:
        from oarepo_rdm.ui.components import (
            CommunitiesMembershipsComponent,
            RDMVocabularyOptionsComponent
        )
        components.append(RDMVocabularyOptionsComponent)
        components.append(CommunitiesMembershipsComponent)
    except ImportError:
        pass
    

    application_id = "dataset"


class DatasetUIResource(RecordsUIResource):
    pass

def ui_overrides(app):
    """Register UI overrides."""
    ui_resource_config = DatasetUIResourceConfig()

    if (
        current_oarepo_ui is not None
        and ui_resource_config.model
        and ui_resource_config.model.record_json_schema
        and ui_resource_config.search_component
    ):
        current_oarepo_ui.register_result_list_item(
            ui_resource_config.model.record_json_schema, ui_resource_config.search_component
        )


def init_menu(app):
    """Initialize menu before first request."""
    ui_resource_config = DatasetUIResourceConfig()

    with app.app_context():
        current_menu.submenu("plus.create_dataset").register(
            f"{ui_resource_config.blueprint_name}.deposit_create",
            _("New Dataset"),
            order=1,
            visible_when=can_view_deposit_page,
        )

def finalize_app(app):
    """Finalize app"""
    init_menu(app)
    ui_overrides(app)

def create_blueprint(app):
    """Register blueprint for this resource."""
    blueprint = DatasetUIResource(DatasetUIResourceConfig()).as_blueprint()
    return blueprint

# TODO: register init_menu to finalize_app similarly blueprints & webpack is registered