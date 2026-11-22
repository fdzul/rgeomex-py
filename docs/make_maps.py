"""Build the interactive maps of the Maps page (docs/maps.md).

mkdocs does not run code, so the maps are made here once and saved as HTML
in docs/assets/maps/; the site only publishes them. Run from the root of the
package after a change:

    python docs/make_maps.py
"""
import re
from pathlib import Path

import geopandas as gpd
import shapely

import rgeomex

OUT = Path(__file__).parent / "assets" / "maps"
OUT.mkdir(parents=True, exist_ok=True)
AMG = ["Guadalajara", "Zapopan", "Tonalá", "Tlaquepaque"]
TILES = "Esri.WorldGrayCanvas"   # light basemap that needs no API key
# the same colour for each locality in every map; the rest in gray
COLORS = {"Guadalajara": "#1b9e77", "Zapopan": "#d95f02", "Tlaquepaque": "#7570b3",
          "Tonalá": "#e7298a", "Other": "#bdbdbd"}


def light(gdf, tol, cols):
    """Keep `cols`, simplify (tol in metres) and round to ~1 m, so the HTML stays small."""
    g = gdf[cols + ["geometry"]].to_crs(6372)
    g["geometry"] = g.geometry.simplify(tol, preserve_topology=True)
    g = g.to_crs(4326)
    g["geometry"] = shapely.set_precision(g.geometry.values, 1e-5)
    return g[~g.geometry.is_empty]


def explore(g, column, caption, tooltip, **kw):
    cats = [c for c in COLORS if c in set(g[column])]
    return g.explore(column=column, categories=cats, cmap=[COLORS[c] for c in cats],
                     tiles=TILES, tooltip=tooltip, legend_kwds={"caption": caption},
                     style_kwds=kw.pop("style_kwds", {"weight": 1, "fillOpacity": 0.6}), **kw)


def save(m, name):
    """Save the map, writing the GeoJSON compactly (no bbox, no spaces in the coordinates)."""
    f = OUT / f"{name}.html"
    m.save(f)
    s = f.read_text(encoding="utf-8")
    s = re.sub(r'"bbox": \[[^\]]*\], ', "", s)
    s = re.sub(r"\[(-?\d+\.?\d*), (-?\d+\.?\d*)\]", r"[\1,\2]", s)
    s = re.sub(r"\], \[", "],[", s)
    f.write_text(s, encoding="utf-8")
    print(f"{name}.html  {f.stat().st_size / 1e6:.1f} MB")


def by_locality(gdf, loc):
    """Name of the locality where each polygon falls (its representative point); 'Other' if none."""
    pts = gpd.GeoDataFrame(geometry=gdf.geometry.representative_point(), crs=gdf.crs)
    j = gpd.sjoin(pts, loc[["NOMGEO", "geometry"]], how="left", predicate="within")
    j = j[~j.index.duplicated()]
    return j["NOMGEO"].fillna("Other").values


# 1. states
states = rgeomex.load("AGEE_inegi19_mx")
save(light(states, 1000, ["CVE_ENT", "NOMGEO"]).explore(
    column="NOMGEO", cmap="tab20", legend=False, tiles=TILES,
    style_kwds={"weight": 1, "fillOpacity": 0.6}, tooltip=["CVE_ENT", "NOMGEO"]), "states")

# 2. municipalities of Jalisco; the four of the metropolitan area in colour
mun = rgeomex.load("AGEM_inegi19_mx", cve_edo="14")
names = {"039": "Guadalajara", "120": "Zapopan", "098": "Tlaquepaque", "101": "Tonalá"}
mun["area"] = mun["CVE_MUN"].map(names).fillna("Other")
save(explore(light(mun, 100, ["CVE_MUN", "NOMGEO", "area"]), "area", "Municipality",
             ["CVE_MUN", "NOMGEO"]), "municipalities")

# 3. the four localities
loc = rgeomex.extract_locality(cve_edo="14", locality=AMG)
save(explore(light(loc, 10, ["CVEGEO", "NOMGEO"]), "NOMGEO", "Locality",
             ["CVEGEO", "NOMGEO"]), "localities")

# 4. AGEB
ageb = rgeomex.extract_ageb(locality=AMG, cve_edo="14")["ageb"]
ageb["locality"] = by_locality(ageb, loc)
save(explore(light(ageb, 5, ["CVEGEO", "locality"]), "locality", "Locality",
             ["CVEGEO", "locality"]), "ageb")

# 5. blocks
blocks = rgeomex.extract_blocks(locality=AMG, cve_edo="14")["block"]
blocks["locality"] = by_locality(blocks.to_crs(loc.crs), loc)
b = light(blocks, 2, ["seccion", "manzana", "locality"])
b[["seccion", "manzana"]] = b[["seccion", "manzana"]].astype(int)
save(explore(b, "locality", "Locality", ["seccion", "manzana"], prefer_canvas=True,
             style_kwds={"weight": 0.3, "fillOpacity": 0.6}), "blocks")
