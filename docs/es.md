# rgeomex en español

Límites geográficos de México para Python: estados, municipios, localidades,
AGEB, manzanas y secciones electorales del INEGI y del INE. Es la versión en
Python del paquete de R [rgeomex](https://github.com/fdzul/rgeomex), parte del
[dengueverse](https://fdzul.r-universe.dev).

Los datos se **descargan bajo demanda**: la primera vez que se usa un conjunto
se descarga del *release* de GitHub, se verifica (SHA-256) y se guarda en una
caché local. Los conjuntos grandes están partidos por estado: si trabajas con
un estado, solo se descarga ese estado.

## Instalación

```bash
pip install rgeomex
```

## Uso

```python
import rgeomex

estados = rgeomex.load("AGEE_inegi19_mx")
municipios = rgeomex.load("AGEM_inegi19_mx", cve_edo="31")

merida = rgeomex.extract_locality(cve_edo="31", locality="Merida")
manzanas = rgeomex.extract_blocks(locality="Merida", cve_edo="31")["block"]
```

Las funciones tienen los mismos nombres que en R: `extract_locality()`,
`extract_blocks()`, `extract_ageb()`, `extract_sectores()` y
`find_most_similar_string()`. El nombre de la localidad se busca de forma
aproximada, así que `"Merida"` encuentra `"Mérida"`. Para la Ciudad de México
(`cve_edo="09"`) se regresan todas sus localidades, igual que en R.

Todas las capas están en EPSG:4326 y el texto en UTF-8. La lista de conjuntos
está en [Datasets](datasets.md) y la documentación de cada función en
[Reference](reference.md).
