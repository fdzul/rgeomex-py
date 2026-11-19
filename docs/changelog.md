# Changelog

## rgeomex 0.1.0 (2026-11-19)

First release of the Python version of rgeomex.

1. Functions `load()`, `datasets()`, `blocks()`, `block_centroids()`, `ageb()`
   and `sectors()`.
2. Functions with the same names and behaviour as in R: `extract_locality()`,
   `extract_blocks()`, `extract_ageb()`, `extract_sectores()` and
   `find_most_similar_string()`.
3. Data downloaded on demand with pooch, verified with SHA-256 and cached
   (`cache_dir()`, `clear_cache()`, environment variable `RGEOMEX_DATA_DIR`).
4. Tests on Linux, macOS and Windows (Python 3.10 and 3.13).

## Data v1 (2026-11-19)

[Release data-v1](https://github.com/fdzul/rgeomex-py/releases/tag/data-v1):
136 GeoParquet files (659 MB) converted from the R package rgeomex 0.1.0.

1. Blocks, block centroids, AGEB and sections split by state (32 files each).
2. Text converted from Latin-1 to UTF-8.
3. Unclosed rings closed and 10 invalid geometries repaired.
4. Same number of rows as in R.
