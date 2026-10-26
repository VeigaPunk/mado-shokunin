#!/usr/bin/env python3
"""Print the source closure of ~/.config/hypr/hyprland.conf, one path per line.

Reuses source-census.py's walker (same module, same order) so the combined run's
--rules order is exactly the census's file order.
"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("census", os.path.join(HERE, "source-census.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

for path in mod.closure(mod.ROOT):
    print(path)
