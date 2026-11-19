# Examples

## 1. A locality and its blocks on a map

```python
import matplotlib.pyplot as plt
import rgeomex

out = rgeomex.extract_blocks(locality="Merida", cve_edo="31")

ax = out["locality"].plot(color="whitesmoke", edgecolor="gray", figsize=(7, 7))
out["block"].boundary.plot(ax=ax, color="steelblue", linewidth=0.1)
ax.set_title(f"Mérida: {len(out['block']):,} blocks (INE 2020)")
ax.set_axis_off()
plt.show()
```

## 2. Blocks within 400 m of a point

The flight range of *Aedes aegypti* (about 400 m) around a point, in metres
with the Mexico ITRF2008 / LCC projection (EPSG:6372):

```python
import geopandas as gpd
from shapely.geometry import Point
import rgeomex

blocks = rgeomex.blocks("31").to_crs(6372)
point = gpd.GeoSeries([Point(-89.62, 20.97)], crs=4326).to_crs(6372)
zone = point.buffer(400).union_all()

near = blocks[blocks.intersects(zone)]
len(near)
```

## 3. Population of the localities (ITER 2020)

`iter_2020_loc` is a table with the population of every locality (2020
Census). Its keys build the 9-digit `CVEGEO` of the locality polygons:

```python
import rgeomex

iter_loc = rgeomex.load("iter_2020_loc")
iter_loc["CVEGEO"] = iter_loc["entidad"] + iter_loc["mun"] + iter_loc["loc"]

loc = rgeomex.load("loc_inegi19_mx", cve_edo="31")
loc = loc.merge(iter_loc[["CVEGEO", "pobtot"]], on="CVEGEO", how="left")
loc[["NOMGEO", "pobtot"]].sort_values("pobtot", ascending=False).head()
```

## 4. Several states at once

```python
peninsula = rgeomex.ageb(["04", "23", "31"])   # Campeche, Quintana Roo, Yucatán
peninsula.groupby("CVE_ENT").size()
```

## 5. Municipalities: 2019 and 2025

```python
m19 = rgeomex.load("AGEM_inegi19_mx", cve_edo="07")
m25 = rgeomex.load("AGEM_inegi25_mx", cve_edo="07")
set(m25["NOMGEO"]) - set(m19["NOMGEO"])        # new municipalities of Chiapas
```

## 6. Export to other formats

```python
out = rgeomex.extract_blocks(locality="Merida", cve_edo="31")
out["block"].to_file("merida_blocks.gpkg")       # GeoPackage (QGIS, R)
out["block"].to_file("merida_blocks.shp")        # shapefile
```
