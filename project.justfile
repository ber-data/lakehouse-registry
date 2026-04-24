## Add your own just recipes here. This is imported by the main justfile.

# Fetch JGI Dremio sources and generate registry YAML
fetch-dremio:
  uv run python src/scripts/fetch_dremio.py --output tests/data/valid/Catalog-JGI-Dremio.yaml
