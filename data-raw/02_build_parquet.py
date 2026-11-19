"""rgeomex-py, data-raw/02_build_parquet.py

Build the GeoParquet files of the release from the export of R
(01_export_from_r.R): the large datasets are split by state, the small ones are
kept whole. Invalid geometries are repaired (make_valid, method "structure").
It also writes the registry (file name + SHA-256) used by the package to
download and verify the files.

Run from the root of the repository:
    python data-raw/02_build_parquet.py
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import geopandas as gpd
import pandas as pd

SRC = Path("data-raw/rgeomex_export")
OUT = Path("data-raw/release")
REGISTRY = Path("src/rgeomex/registry.txt")

# datasets split by state: name -> (parts in R, state column)
SPLIT = {
    "AGEB_inegi_2019": (["AGEB_inegi_2019_a", "AGEB_inegi_2019_b"], "CVE_ENT"),
    "blocks_ine20_mx": ([f"blocks_ine20_mx_{p}" for p in "abcde"], "entidad"),
    "sectores_ine20_mx": ([f"sectores_ine20_mx_{p}" for p in "abc"], "entidad"),
}
# whole datasets (sf in R)
WHOLE = ["AGEE_inegi19_mx", "AGEM_inegi19_mx", "AGEM_inegi25_mx",
         "loc_inegi19_mx", "hrl_mx", "pua_mx", "ua_mx"]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write(gdf, name: str, rows: list) -> None:
    f = OUT / f"{name}.parquet"
    invalid = repaired = crs = None
    if isinstance(gdf, gpd.GeoDataFrame):
        bad = ~gdf.geometry.is_valid
        invalid = int(bad.sum())
        if invalid:
            # repair only the invalid geometries; "structure" keeps them polygonal
            gdf = gdf.copy()
            gdf.loc[bad, "geometry"] = gdf.loc[bad, "geometry"].make_valid(
                method="structure", keep_collapsed=False)
        repaired = invalid - int((~gdf.geometry.is_valid).sum())
        crs = gdf.crs.to_epsg() if gdf.crs else None
    gdf.to_parquet(f, compression="zstd", index=False)
    rows.append({"file": f.name, "rows": len(gdf), "crs": crs,
                 "invalid_geometries": invalid, "repaired": repaired,
                 "mb": round(f.stat().st_size / 1e6, 2), "sha256": sha256(f)})
    print(f"{f.name}: {len(gdf)} rows, {rows[-1]['mb']} MB")


def state_key(s: pd.Series) -> pd.Series:
    """State key as two-digit text ("01".."32")."""
    return pd.to_numeric(s, errors="coerce").astype("Int64").astype(str).str.zfill(2)


def read(name: str) -> gpd.GeoDataFrame:
    # on_invalid="fix" closes the rings that are not closed (sectores)
    return gpd.read_file(SRC / f"{name}.gpkg", on_invalid="fix")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows: list = []

    # 1. whole datasets
    for name in WHOLE:
        write(read(name), name, rows)

    # 2. datasets split by state
    for name, (parts, col) in SPLIT.items():
        gdf = pd.concat([read(p) for p in parts], ignore_index=True)
        gdf = gpd.GeoDataFrame(gdf, geometry="geometry", crs=4326)
        key = state_key(gdf[col])
        for edo in sorted(key.dropna().unique()):
            write(gdf[key == edo], f"{name}_{edo}", rows)

    # 3. block centroids: points, split by state
    cen = pd.read_csv(SRC / "blocks_ine20_mx_centroid.csv",
                      dtype={"cve_ent": str, "cve_geo": str})
    cen = gpd.GeoDataFrame(cen, geometry=gpd.points_from_xy(cen["x"], cen["y"]),
                           crs=4326)
    key = state_key(cen["cve_ent"])
    for edo in sorted(key.dropna().unique()):
        write(cen[key == edo], f"blocks_ine20_mx_centroid_{edo}", rows)

    # 4. ITER 2020 localities: table with the INEGI keys as text
    iter_loc = pd.read_csv(SRC / "iter_2020_loc.csv",
                           dtype={"entidad": str, "mun": str, "loc": str})
    write(iter_loc, "iter_2020_loc", rows)

    # 5. manifest and registry
    man = pd.DataFrame(rows)
    man.to_csv(OUT / "manifest.csv", index=False)
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY.write_text("".join(f"{r['file']} sha256:{r['sha256']}\n" for r in rows))
    print(f"\n{len(man)} files, {man['mb'].sum():.0f} MB in {OUT}")
    print(f"invalid geometries: {int(man['invalid_geometries'].fillna(0).sum())}, "
          f"repaired: {int(man['repaired'].fillna(0).sum())}")


if __name__ == "__main__":
    main()
