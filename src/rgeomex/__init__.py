"""rgeomex: geographic boundaries of Mexico (INEGI, INE) for Python.

Python version of the R package rgeomex (https://github.com/fdzul/rgeomex).
The data are downloaded on demand from the GitHub release and cached locally.
"""
from ._data import (ageb, block_centroids, blocks, cache_dir, clear_cache,
                    datasets, load, sectors, state_code)
from ._extract import (extract_ageb, extract_blocks, extract_locality,
                       extract_sectores, find_most_similar_string)

__version__ = "0.1.0"

__all__ = [
    "load", "datasets", "blocks", "block_centroids", "ageb", "sectors",
    "extract_locality", "extract_blocks", "extract_ageb", "extract_sectores",
    "find_most_similar_string", "state_code", "cache_dir", "clear_cache",
]
