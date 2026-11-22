# Maps

Interactive maps of the polygons of rgeomex, from the whole country down to
the blocks of the metropolitan area of Guadalajara (the localities of
Guadalajara, Zapopan, Tlaquepaque and Tonalá). Each map shows the code that
makes it; zoom in and hover over a polygon to see its keys.

The maps were made with `.explore()` of geopandas; the script that builds
them is [`docs/make_maps.py`](https://github.com/fdzul/rgeomex-py/blob/main/docs/make_maps.py).

```python
import rgeomex

amg = ["Guadalajara", "Zapopan", "Tonalá", "Tlaquepaque"]
```

## States

```python
states = rgeomex.load("AGEE_inegi19_mx")
states.explore(column="NOMGEO", legend=False)
```

<iframe src="../assets/maps/states.html" width="100%" height="520" style="border:0" loading="lazy"></iframe>

## Municipalities

The 125 municipalities of Jalisco; the four of the metropolitan area in colour.

```python
mun = rgeomex.load("AGEM_inegi19_mx", cve_edo="14")
mun.explore(tooltip=["CVE_MUN", "NOMGEO"])
```

<iframe src="../assets/maps/municipalities.html" width="100%" height="520" style="border:0" loading="lazy"></iframe>

## Localities

```python
loc = rgeomex.extract_locality(cve_edo="14", locality=amg)
loc.explore(column="NOMGEO")
```

<iframe src="../assets/maps/localities.html" width="100%" height="520" style="border:0" loading="lazy"></iframe>

## AGEB

The urban AGEB (INEGI 2019) that intersect the four localities, coloured by
the locality where they fall.

```python
ageb = rgeomex.extract_ageb(locality=amg, cve_edo="14")
ageb["ageb"].explore(tooltip=["CVEGEO"])
```

<iframe src="../assets/maps/ageb.html" width="100%" height="520" style="border:0" loading="lazy"></iframe>

## Blocks

The blocks (INE 2020) of the four localities, about 40,000 polygons; the map
can take a few seconds to load.

```python
blocks = rgeomex.extract_blocks(locality=amg, cve_edo="14")
blocks["block"].explore(tooltip=["seccion", "manzana"])
```

<iframe src="../assets/maps/blocks.html" width="100%" height="520" style="border:0" loading="lazy"></iframe>
