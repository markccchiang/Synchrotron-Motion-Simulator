"""Put ../src on sys.path so these scripts can import BasicFunc and Input.

The scripts live in examples/ while the physics module and its configuration
live in src/. Importing this module first adds src/ to the import path, which
lets a bare `python examples/<script>.py` work from anywhere without requiring
PYTHONPATH to be set.
"""
import os
import sys

_SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'src')
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)
