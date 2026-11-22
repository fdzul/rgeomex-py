"""Tests with small local files (no download)."""
import hashlib

import geopandas as gpd
import pandas as pd
import pooch
import pytest
from shapely.geometry import Point, box

import rgeomex
from rgeomex import _data


@pytest.fixture()
def local_data(tmp_path, monkeypatch):
    loc = gpd.GeoDataFrame(
        {"CVEGEO": ["310500001", "310890001", "090010001"],
         "CVE_ENT": ["31", "31", "09"], "CVE_MUN": ["050", "089", "001"],
         "CVE_LOC": ["0001", "0001", "0001"],
         "NOMGEO": ["Mérida", "Ticul", "Álvaro Obregón"], "AMBITO": "Urbana"},
        geometry=[box(0, 0, 10, 10), box(20, 0, 30, 10), box(40, 0, 50, 10)], crs=4326)
    blk = gpd.GeoDataFrame({"entidad": [31, 31, 31], "manzana": [1, 2, 3]},
                           geometry=[box(1, 1, 2, 2), box(21, 1, 22, 2), box(60, 60, 61, 61)],
                           crs=4326)
    files = {"loc_inegi19_mx.parquet": loc, "blocks_ine20_mx_31.parquet": blk}
    reg = {}
    for name, gdf in files.items():
        gdf.to_parquet(tmp_path / name)
        reg[name] = "sha256:" + hashlib.sha256((tmp_path / name).read_bytes()).hexdigest()
    fetcher = pooch.create(path=tmp_path, base_url="https://example.invalid/", registry=reg)
    _data._fetcher.cache_clear()
    monkeypatch.setattr(_data, "_fetcher", lambda: fetcher)
    return tmp_path


def test_state_code():
    assert rgeomex.state_code(31) == "31"
    assert rgeomex.state_code("031") == "31"
    assert rgeomex.state_code("9") == "09"
    with pytest.raises(ValueError):
        rgeomex.state_code(33)


def test_find_most_similar_string():
    t = ["Mérida", "Ticul", "Umán"]
    assert rgeomex.find_most_similar_string("Merida", t) == "Mérida"
    assert rgeomex.find_most_similar_string(["ticul", "Uman"], t) == ["Ticul", "Umán"]
    with pytest.warns(UserWarning):
        assert rgeomex.find_most_similar_string("x", ["ab", "ac"]) is None


def test_load_and_filter(local_data):
    loc = rgeomex.load("loc_inegi19_mx", cve_edo=31)
    assert len(loc) == 2 and loc.crs.to_epsg() == 4326
    with pytest.raises(ValueError):
        rgeomex.load("blocks_ine20_mx")          # needs cve_edo
    with pytest.raises(ValueError):
        rgeomex.load("no_existe")


def test_extract_locality_and_blocks(local_data):
    loc = rgeomex.extract_locality("31", "Merida")
    assert loc["NOMGEO"].tolist() == ["Mérida"]
    out = rgeomex.extract_blocks("Merida", "31")
    assert out["block"]["manzana"].tolist() == [1]
    cdmx = rgeomex.extract_locality("09")
    assert len(cdmx) == 1


def test_extract_several_localities(local_data):
    loc = rgeomex.extract_locality("31", ["Merida", "Ticul"])
    assert sorted(loc["NOMGEO"]) == ["Mérida", "Ticul"]
    out = rgeomex.extract_blocks(["Merida", "Ticul"], "31")
    assert sorted(out["block"]["manzana"]) == [1, 2]


def test_datasets():
    d = rgeomex.datasets()
    assert {"blocks_ine20_mx", "AGEE_inegi19_mx"} <= set(d["dataset"])
