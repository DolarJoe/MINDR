# Agent Guide for MINDR

> **Generated:** 2026-06-23  

---

## 1. Project Overview

**MINDR** (Multimodal Imaging and Data Repository) is an [OARepo](https://github.com/oarepo)/[InvenioRDM](https://inveniosoftware.org/products/rdm/) based data repository instance.

- **Short name:** `MINDR`
- **Python version:** `>=3.14,<3.15`
- **Package manager:** `uv` (lockfile: `uv.lock`)
- **Build runner:** `./run.sh` (fetches `.runner.sh` from the OARepo GitHub org if missing)
- **Primary model:** `dataset` — a generic dataset record model registered from `models/dataset/model.py`

The repository was bootstrapped from the `nrp-app-copier` Copier template (`oarepo/nrp-app-copier`, commit `8cc8598`) with `use_ccmm: true`.

---

## 2. Repository Status

### What currently exists

- A default `dataset` model in `models/dataset/`
  - `metadata.yaml` defines only `title` and `languages`.
  - Custom permission policy allows authenticated users to view the deposit page.
  - DataCite JSON export is wired up via `DataCiteJSONSerializer`.
- UI layer for the dataset at `ui/dataset/`
  - Semantic UI templates (deposit create/edit, search, record detail, tombstone)
  - Webpack entries for search and deposit form
  - `DatasetUIResourceConfig` registers `/dataset` URLs
- i18n scaffolding, translations, fixtures (languages, rights, communities, etc.)
- Docker Compose for local services (PostgreSQL, Redis, RabbitMQ, OpenSearch, MinIO)
- `invenio.cfg` with OARepo configuration helpers

---

## 3. Repository Structure

```
.
├── app_data/                 # Runtime app data (empty pages folder)
├── assets/less/site/         # Site-wide LESS overrides for Semantic UI
├── common/                   # Shared Python packages used by models/UIs
│   ├── alembic/              # Alembic migration support
│   └── workflows/default.py  # OARepo workflow permission/transition policy
├── docker/                   # docker-compose.yml, dev certs, uwsgi config
├── fixtures/                 # YAML fixtures for vocabularies, rights, etc.
├── i18n/                     # i18n webpack bundle and translation init
├── models/dataset/           # Dataset model definition
│   ├── metadata.yaml         # Field schema
│   ├── model.py              # Model builder registration
│   └── serializers.py        # DataCite export serializer
├── static/images/            # Static image assets
├── templates/                # Global Jinja templates / overrides
├── translations/             # Compiled .po/.pot files
├── ui/dataset/               # Dataset UI resource and templates
│   ├── __init__.py           # Resource config, blueprint, menu registration
│   ├── semantic-ui/js/       # React JSX for deposit form and search
│   ├── templates/semantic-ui/# Jinja templates
│   └── webpack.py            # Webpack theme bundle
├── invenio.cfg               # Main Invenio config
├── pyproject.toml            # Project metadata, entry points, build system
├── run.sh                    # OARepo repository runner entrypoint
├── variables                 # Environment variables for local development
└── uv.lock                   # Locked dependency tree
```

---

## 4. Tech Stack

| Layer          | Technology                           |
| -------------- | ------------------------------------ |
| Framework      | InvenioRDM / OARepo                  |
| Language       | Python 3.14                          |
| Package/venv   | `uv` + `uv_build`                    |
| DB             | PostgreSQL 15                        |
| Search         | OpenSearch 2                         |
| Cache / broker | Redis 7, RabbitMQ 3                  |
| Object storage | MinIO (S3-compatible)                |
| Frontend       | Semantic UI React, custom JSX        |
| Task queue     | Celery (beat schedule files present) |

### Key dependencies

```toml
oarepo[s3,rdm]>=14.0.0b1,<15.0.0
oarepo-app[production,ccmm]>=2.0.1,<3.0.0
```

---

## 5. Entry Points

The project registers the following Invenio entry points (see `pyproject.toml`):

- `invenio_assets.webpack`
  - `i18n` → `i18n.webpack:theme`
  - `components` → `ui.components.webpack:theme`
  - `ui_dataset` → `ui.dataset.webpack:theme`
- `invenio_i18n.translations`
  - `translations` → `i18n`
- `invenio_db.alembic`
  - `repository` → `common:alembic`
- `invenio_base.blueprints`
  - `ui_dataset` → `ui.dataset:create_blueprint`
- `invenio_base.finalize_app`
  - `ui_dataset` → `ui.dataset:finalize_app`

---

## 6. Local Development

### Configure the environment

```bash
source .venv/bin/activate
# or
uv run ...
```

### Start backing services

```bash
./run.sh run
```

### Help in

```bash
./run.sh --help
```

### Ports (from `variables` and `.invenio.private`)

| Service              | Port  |
| -------------------- | ----- |
| Web / API            | 5000  |
| PostgreSQL           | 5632  |
| Redis                | 6579  |
| RabbitMQ (AMQP)      | 5872  |
| RabbitMQ Management  | 15872 |
| OpenSearch           | 9400  |
| OpenSearch Dashboard | 5801  |
| MinIO API            | 9000  |
| MinIO Console        | 9001  |

---

## 7. Conventions for Agents

### When adding a metadata field

1. Edit `models/dataset/metadata.yaml`.
2. Add or update the corresponding deposit form JSX under `ui/dataset/semantic-ui/js/dataset/forms/`.
3. Update search result item and record detail templates under `ui/dataset/templates/semantic-ui/dataset/`.
4. Regenerate models / records (usually via `./run.sh` or OARepo tooling).
5. Update translations with `babel` if user-facing labels changed.
6. Add an Alembic migration in `common/alembic/` if the database schema changes.

### When editing UI

- Templates live under `ui/dataset/templates/semantic-ui/dataset/`.
- JSX components live under `ui/dataset/semantic-ui/js/dataset/`.
- Site-wide LESS overrides go in `assets/less/site/globals/`.
- Static assets go in `static/images/`.

### When editing config

- Application config: `invenio.cfg`
- Environment variables: `variables`
- Private instance config: `.invenio.private`

### Do not

- Delete `uv.lock` unless you intend to regenerate dependencies.
- Hard-code enum keyword lists in multiple places; prefer vocabulary fixtures or shared config.
- Ignore translation files when adding user-facing strings.

---

## 8. Known Issues / Watchouts

1. **Placeholder description.** The Copier-generated description is still a placeholder in `README.md`, `pyproject.toml`, and `invenio.cfg`.
2. **Empty schema.** The `dataset` model is currently minimal. The next logical work is to expand `models/dataset/metadata.yaml` and the corresponding UI.
3. **Celery beat schedule files** (`celerybeat-schedule*`) are present in the working directory; they are generated at runtime and should normally be ignored.

---

## 9. Suggested Next Steps

1. Clarify which metadata fields from `specs/metadata_fields.md` / `specs/missing_metadata_fields.md` are actually intended for this repository.
2. Expand `models/dataset/metadata.yaml` defined by the user (ask them).
3. Update deposit form, search, and record-detail UI for the new fields.
4. Add/refresh fixtures for controlled vocabularies (languages already exists; imaging modality, disease, species, etc. may be needed).
5. Replace placeholder description with real project copy.
