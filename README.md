# rgeomex

**English** | [Español](#español)

Geographic boundaries of Mexico for Python: states, municipalities, localities,
AGEB, blocks (*manzanas*) and electoral sections, from INEGI and INE. It is the
Python version of the R package [rgeomex](https://github.com/fdzul/rgeomex),
part of the [dengueverse](https://fdzul.github.io/dengueverse/).

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

## Usage

```python
import rgeomex

rgeomex.datasets()                                   # available datasets

states = rgeomex.load("AGEE_inegi19_mx")             # 32 states
mun = rgeomex.load("AGEM_inegi19_mx", cve_edo="31")  # municipalities of Yucatán

merida = rgeomex.extract_locality(cve_edo="31", locality="Merida")
blk = rgeomex.extract_blocks(locality="Merida", cve_edo="31")
blk["block"]                                         # blocks of Mérida

rgeomex.blocks("31")                                 # all the blocks of Yucatán
rgeomex.ageb(["31", "23"])                           # AGEB of Yucatán and Quintana Roo
```

All the layers are in EPSG:4326 and the text is UTF-8.

## Datasets

| Dataset | Content | Source | Split by state |
|---|---|---|---|
| `AGEE_inegi19_mx` | States | INEGI 2019 | no |
| `AGEM_inegi19_mx`, `AGEM_inegi25_mx` | Municipalities | INEGI 2019, 2025 | no |
| `loc_inegi19_mx` | Urban localities | INEGI 2019 | no |
| `iter_2020_loc` | Localities (ITER), with population (table) | INEGI, Census 2020 | no |
| `AGEB_inegi_2019` | Urban AGEB | INEGI 2019 | yes |
| `blocks_ine20_mx` | Blocks | INE 2020 | yes |
| `blocks_ine20_mx_centroid` | Centroids of the blocks | INE 2020 | yes |
| `sectores_ine20_mx` | Electoral sections | INE 2020 | yes |
| `hrl_mx`, `pua_mx`, `ua_mx` | Other layers of rgeomex | | no |

The cache folder is `rgeomex.cache_dir()`; set the environment variable
`RGEOMEX_DATA_DIR` to use another folder (for example, one that already has
the files, for offline use).

## Credits

Original shapefiles are created by official government institutions
([INEGI](https://www.inegi.org.mx/temas/mg) and
[INE](https://pautas.ine.mx/transparencia/mapas/)). The files were converted
from rgeomex (R) to GeoParquet with the scripts in `data-raw/`; the text was
converted to UTF-8 and 10 invalid geometries were repaired.

## License

MIT.

---

## Español

Límites geográficos de México para Python: estados, municipios, localidades,
AGEB, manzanas y secciones electorales del INEGI y del INE. Es la versión en
Python del paquete de R [rgeomex](https://github.com/fdzul/rgeomex).

Los datos se **descargan bajo demanda**: la primera vez que se usa un conjunto
se descarga del *release* de GitHub, se verifica y se guarda en una caché
local. Los conjuntos grandes están partidos por estado: si trabajas con un
estado, solo se descarga ese estado.

```python
import rgeomex

merida = rgeomex.extract_locality(cve_edo="31", locality="Merida")
manzanas = rgeomex.extract_blocks(locality="Merida", cve_edo="31")["block"]
```

Las funciones tienen los mismos nombres que en R (`extract_locality()`,
`extract_blocks()`, `extract_ageb()`, `extract_sectores()`,
`find_most_similar_string()`). Todas las capas están en EPSG:4326 y el texto
en UTF-8.
