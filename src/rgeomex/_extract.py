"""Extract a locality and its blocks, AGEB or sections (as in rgeomex for R)."""
from __future__ import annotations

import warnings

import geopandas as gpd

from ._data import ageb, blocks, load, sectors, state_code


def _levenshtein(a: str, b: str) -> int:
    """Generalized Levenshtein distance (insertions, deletions, substitutions)."""
    if len(a) < len(b):
        a, b = b, a
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def find_most_similar_string(s, t, max_dist=float("inf"), ignore_case=True,
                             verbose=True, feeling_lucky=False):
    """Most similar string of ``t`` for each string of ``s`` (Levenshtein).

    Same behaviour as ``rgeomex::find_most_similar_string()`` in R: returns
    ``None`` when no string is within ``max_dist`` or when there is a tie
    (unless ``feeling_lucky=True``, which returns the first one).
    """
    single = isinstance(s, str)
    s = [s] if single else list(s)
    t = [x for x in dict.fromkeys(t) if isinstance(x, str)]
    out = []
    for e in s:
        if e is None:
            out.append(None)
            continue
        ee = e.lower() if ignore_case else e
        d = [(_levenshtein(ee, x.lower() if ignore_case else x), x) for x in t]
        d = [p for p in d if p[0] <= max_dist]
        if not d:
            if verbose:
                warnings.warn(f"No similar string below threshold found for {e!r}.")
            out.append(None)
            continue
        best = min(p[0] for p in d)
        hits = [x for dist, x in d if dist == best]
        if len(hits) > 1 and not feeling_lucky:
            if verbose:
                warnings.warn(f"No single most similar string found for {e!r}: {hits}.")
            out.append(None)
        else:
            out.append(hits[0])
    return out[0] if single else out


def extract_locality(cve_edo, locality: str | None = None) -> gpd.GeoDataFrame:
    """Boundary of a locality (INEGI 2019), found by its approximate name.

    For Mexico City (``cve_edo = "09"``) all its localities are returned.
    """
    edo = state_code(cve_edo)
    loc = load("loc_inegi19_mx", edo)
    if edo == "09":
        return loc
    if locality is None:
        raise ValueError("give the name of the locality")
    name = find_most_similar_string(locality, loc["NOMGEO"].tolist())
    if name is None:
        raise ValueError(f"locality {locality!r} not found in state {edo}")
    return loc[loc["NOMGEO"] == name].reset_index(drop=True)


def _within_locality(layer, cve_edo, locality):
    loc = extract_locality(cve_edo, locality)
    y = layer(state_code(cve_edo))
    y = y[y.intersects(loc.union_all())].reset_index(drop=True)
    return loc, y


def extract_blocks(locality, cve_edo) -> dict:
    """Blocks (INE 2020) that intersect a locality: ``{"locality", "block"}``."""
    loc, y = _within_locality(blocks, cve_edo, locality)
    return {"locality": loc, "block": y}


def extract_ageb(locality, cve_edo) -> dict:
    """AGEB (INEGI 2019) that intersect a locality: ``{"locality", "ageb"}``."""
    loc, y = _within_locality(ageb, cve_edo, locality)
    return {"locality": loc, "ageb": y}


def extract_sectores(locality, cve_edo) -> dict:
    """Sections (INE 2020) that intersect a locality: ``{"locality", "sectores"}``."""
    loc, y = _within_locality(sectors, cve_edo, locality)
    return {"locality": loc, "sectores": y}
