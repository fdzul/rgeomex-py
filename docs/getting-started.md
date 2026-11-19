# Getting Started

## Installation

```bash
pip install rgeomex
# development version
pip install git+https://github.com/fdzul/rgeomex-py
```

rgeomex needs Python 3.10 or later; it installs geopandas, pyarrow and pooch.

## Load a dataset

```python
import rgeomex

rgeomex.datasets()                                   # the available datasets

states = rgeomex.load("AGEE_inegi19_mx")             # 32 states
mun = rgeomex.load("AGEM_inegi19_mx", cve_edo="31")  # municipalities of Yucatán
```

The state key (`cve_edo`) is the INEGI key, `"01"` to `"32"`; `31`, `"31"` or
`"031"` are all accepted.

## Extract a locality

```python
merida = rgeomex.extract_locality(cve_edo="31", locality="Merida")
```

The name is found approximately (Levenshtein distance, case insensitive), so
`"Merida"` finds `"Mérida"`. If two names are equally close, `None` is
returned with a warning, as in R. For Mexico City (`cve_edo="09"`) all its
localities are returned.

## Blocks, AGEB and sections of a locality

```python
out = rgeomex.extract_blocks(locality="Merida", cve_edo="31")
out["locality"]   # boundary of the locality
out["block"]      # blocks (INE 2020) that intersect it

rgeomex.extract_ageb(locality="Merida", cve_edo="31")["ageb"]
rgeomex.extract_sectores(locality="Merida", cve_edo="31")["sectores"]
```

## The cache

The first time a dataset is used it is downloaded from the
[GitHub release](https://github.com/fdzul/rgeomex-py/releases/tag/data-v1);
later it is read from the cache.

```python
rgeomex.cache_dir()    # e.g. ~/Library/Caches/rgeomex on macOS
rgeomex.clear_cache()  # delete the downloaded files
```

To use another folder, or a folder that already has the files (offline use),
set the environment variable `RGEOMEX_DATA_DIR` before importing rgeomex:

```bash
export RGEOMEX_DATA_DIR=/path/to/rgeomex_data
```
