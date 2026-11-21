# rgeomex <img src="assets/logo.png" align="right" height="139" alt="" />

**Geographic boundaries of Mexico for Python**: states, municipalities,
localities, AGEB, blocks (*manzanas*) and electoral sections, from INEGI and
INE. It is the Python version of the R package
[rgeomex](https://github.com/fdzul/rgeomex), part of the
[dengueverse](https://fdzul.r-universe.dev).

```python
import rgeomex

merida = rgeomex.extract_locality(cve_edo="31", locality="Merida")
blocks = rgeomex.extract_blocks(locality="Merida", cve_edo="31")["block"]
len(blocks)   # 15,374 blocks
```

## Features

1. **Data on demand:** each dataset is downloaded the first time it is used,
   verified (SHA-256) and kept in a local cache.
2. **Split by state:** the large datasets (blocks, AGEB, sections) are one file
   per state, so working with one state downloads only that state.
3. **Same functions as in R:** `extract_locality()`, `extract_blocks()`,
   `extract_ageb()`, `extract_sectores()` and `find_most_similar_string()`.
4. **Clean data:** EPSG:4326, text in UTF-8 and invalid geometries repaired.
5. **GeoParquet + geopandas:** every layer is a `GeoDataFrame`.

## Next

1. [Getting Started](getting-started.md): installation and first steps.
2. [Examples](examples.md): complete use cases.
3. [Datasets](datasets.md): the layers available.
4. [Citation](citation.md): how to cite the package.
