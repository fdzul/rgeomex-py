"""Download (once) and read the rgeomex datasets.

The GeoParquet files live in a GitHub release of fdzul/rgeomex-py. Each file
is downloaded the first time it is used, verified with its SHA-256 and kept in
a local cache. Set the environment variable ``RGEOMEX_DATA_DIR`` to use another
cache folder, or a folder that already has the files (offline use).
"""
from __future__ import annotations

import os
from functools import lru_cache
from importlib import resources
from pathlib import Path

import geopandas as gpd
import pandas as pd
import pooch

DATA_TAG = "data-v1"
BASE_URL = f"https://github.com/fdzul/rgeomex-py/releases/download/{DATA_TAG}/"

#: datasets split by state (one file per state, "01".."32")
BY_STATE = ("AGEB_inegi_2019", "blocks_ine20_mx", "blocks_ine20_mx_centroid",
            "sectores_ine20_mx")
#: whole datasets
WHOLE = ("AGEE_inegi19_mx", "AGEM_inegi19_mx", "AGEM_inegi25_mx",
         "loc_inegi19_mx", "hrl_mx", "pua_mx", "ua_mx", "iter_2020_loc")
#: tables without geometry
TABLES = ("iter_2020_loc",)


def _registry() -> dict[str, str]:
    txt = resources.files("rgeomex").joinpath("registry.txt").read_text()
    reg = {}
    for line in txt.splitlines():
        if line.strip():
            name, sha = line.split()
            reg[name] = sha
    return reg


@lru_cache(maxsize=1)
def _fetcher() -> pooch.Pooch:
    path = os.environ.get("RGEOMEX_DATA_DIR") or pooch.os_cache("rgeomex")
    return pooch.create(path=path, base_url=BASE_URL, registry=_registry(),
                        retry_if_failed=2)


def cache_dir() -> Path:
    """Folder where the downloaded files are kept."""
    return Path(_fetcher().abspath)


def clear_cache() -> None:
    """Delete the downloaded files (they are downloaded again when needed)."""
    for f in cache_dir().glob("*.parquet"):
        f.unlink()


def state_code(cve_edo: str | int) -> str:
    """INEGI state key as two-digit text: 31, "31" or "031" -> "31"."""
    try:
        n = int(str(cve_edo).strip())
    except ValueError as e:
        raise ValueError(f"cve_edo must be a state key from 01 to 32, not {cve_edo!r}") from e
    if not 1 <= n <= 32:
        raise ValueError(f"cve_edo must be a state key from 01 to 32, not {cve_edo!r}")
    return f"{n:02d}"


def _read(file: str) -> gpd.GeoDataFrame | pd.DataFrame:
    path = _fetcher().fetch(file)
    if file.removesuffix(".parquet") in TABLES:
        return pd.read_parquet(path)
    return gpd.read_parquet(path)


def datasets() -> pd.DataFrame:
    """Table of the available datasets."""
    rows = [{"dataset": d, "by_state": False, "geometry": d not in TABLES}
            for d in WHOLE]
    rows += [{"dataset": d, "by_state": True, "geometry": True} for d in BY_STATE]
    return pd.DataFrame(rows)


def load(dataset: str, cve_edo: str | int | list | None = None):
    """Load a dataset by its name in rgeomex (R).

    Parameters
    ----------
    dataset : str
        Name of the dataset, e.g. ``"AGEE_inegi19_mx"`` or ``"blocks_ine20_mx"``
        (see :func:`datasets`).
    cve_edo : str, int or list, optional
        INEGI state key(s). Required for the datasets split by state
        (``AGEB_inegi_2019``, ``blocks_ine20_mx``, ``blocks_ine20_mx_centroid``,
        ``sectores_ine20_mx``); for the whole datasets it filters the rows of
        the state when the dataset has a ``CVE_ENT`` or ``entidad`` column.
    """
    if dataset in BY_STATE:
        if cve_edo is None:
            raise ValueError(f"{dataset} is split by state: give cve_edo (01 to 32)")
        keys = cve_edo if isinstance(cve_edo, (list, tuple)) else [cve_edo]
        parts = [_read(f"{dataset}_{state_code(k)}.parquet") for k in keys]
        return parts[0] if len(parts) == 1 else pd.concat(parts, ignore_index=True)
    if dataset in WHOLE:
        x = _read(f"{dataset}.parquet")
        if cve_edo is not None:
            keys = cve_edo if isinstance(cve_edo, (list, tuple)) else [cve_edo]
            keys = [state_code(k) for k in keys]
            col = next((c for c in ("CVE_ENT", "entidad") if c in x.columns), None)
            if col is None:
                raise ValueError(f"{dataset} has no state column to filter by cve_edo")
            x = x[x[col].astype(str).str.zfill(2).isin(keys)].reset_index(drop=True)
        return x
    raise ValueError(f"unknown dataset {dataset!r}; see rgeomex.datasets()")


def blocks(cve_edo):
    """INE 2020 blocks (manzanas) of one or several states."""
    return load("blocks_ine20_mx", cve_edo)


def block_centroids(cve_edo):
    """Centroids of the INE 2020 blocks of one or several states."""
    return load("blocks_ine20_mx_centroid", cve_edo)


def ageb(cve_edo):
    """INEGI 2019 AGEB of one or several states."""
    return load("AGEB_inegi_2019", cve_edo)


def sectors(cve_edo):
    """INE 2020 electoral sections (secciones) of one or several states."""
    return load("sectores_ine20_mx", cve_edo)
