# Datasets

| Dataset | Content | Source | Split by state | Rows |
|---|---|---|---|---|
| `AGEE_inegi19_mx` | States | INEGI 2019 | no | 32 |
| `AGEM_inegi19_mx` | Municipalities | INEGI 2019 | no | 2,465 |
| `AGEM_inegi25_mx` | Municipalities | INEGI 2025 | no | 2,478 |
| `loc_inegi19_mx` | Urban localities | INEGI 2019 | no | 4,553 |
| `iter_2020_loc` | Localities (ITER) with population, table | INEGI, Census 2020 | no | 189,432 |
| `AGEB_inegi_2019` | Urban AGEB | INEGI 2019 | yes | 62,732 |
| `blocks_ine20_mx` | Blocks (*manzanas*) | INE 2020 | yes | 1,556,070 |
| `blocks_ine20_mx_centroid` | Centroids of the blocks | INE 2020 | yes | 1,556,070 |
| `sectores_ine20_mx` | Electoral sections | INE 2020 | yes | 68,436 |
| `hrl_mx` | Layer of rgeomex | | no | 150 |
| `pua_mx` | Layer of rgeomex | | no | 111 |
| `ua_mx` | Layer of rgeomex | | no | 658 |

The datasets split by state need `cve_edo` (INEGI key, `"01"` to `"32"`):

```python
rgeomex.blocks("31")                 # Yucatán
rgeomex.ageb(["31", "23"])           # Yucatán and Quintana Roo
rgeomex.load("sectores_ine20_mx", cve_edo=20)
```

## How the files were made

The files were converted from rgeomex (R) with the scripts in
[`data-raw/`](https://github.com/fdzul/rgeomex-py/tree/main/data-raw):

1. `01_export_from_r.R` exports each dataset and converts the text from
   Latin-1 to UTF-8.
2. `02_build_parquet.py` splits the large datasets by state, writes GeoParquet
   (zstd), repairs the invalid geometries (10 in total) and writes the registry
   of SHA-256 checksums.

The row counts are the same as in R.
