# rgeomex

Geographic boundaries of Mexico for Python: states, municipalities, localities,
AGEB, blocks (*manzanas*) and electoral sections, from INEGI and INE. It is the
Python version of the R package [rgeomex](https://github.com/fdzul/rgeomex),
part of the [dengueverse](https://fdzul.r-universe.dev).

The data are **downloaded on demand**: the first time a dataset is used it is
downloaded from the [GitHub release](https://github.com/fdzul/rgeomex-py/releases),
verified (SHA-256) and kept in a local cache. The large datasets are split by
state, so working with one state downloads only that state.

## Installation

```bash
pip install rgeomex
# development version
pip install git+https://github.com/fdzul/rgeomex-py
```

## Quick start

```python
import rgeomex

states = rgeomex.load("AGEE_inegi19_mx")             # 32 states
mun = rgeomex.load("AGEM_inegi19_mx", cve_edo="31")  # municipalities of Yucatán

merida = rgeomex.extract_locality(cve_edo="31", locality="Merida")
blocks = rgeomex.extract_blocks(locality="Merida", cve_edo="31")["block"]
len(blocks)                                          # 15,374 blocks
```

The name of the locality is found approximately (Levenshtein distance, case
insensitive), so `"Merida"` finds `"Mérida"`. For Mexico City (`cve_edo="09"`)
all its localities are returned, as in R.

All the layers are in EPSG:4326 and the text is UTF-8.

## Cache

```python
rgeomex.cache_dir()    # folder of the downloaded files
rgeomex.clear_cache()  # delete them (they are downloaded again when needed)
```

Set the environment variable `RGEOMEX_DATA_DIR` to use another folder, for
example one that already has the files, for offline use.

## Credits

Original shapefiles are created by official government institutions
([INEGI](https://www.inegi.org.mx/temas/mg) and
[INE](https://pautas.ine.mx/transparencia/mapas/)).
