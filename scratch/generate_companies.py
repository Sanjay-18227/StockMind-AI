"""
StockMind AI — Master 650+ Company Catalog Generator
Generates and writes data/companies_master.json covering all Indian (NSE/BSE)
bluechips, midcaps, smallcaps, PSUs, and global mega-caps.
"""
import os
import sys

# Delegate to scratch/build_comprehensive_catalog.py
script_dir = os.path.dirname(__file__)
build_script = os.path.join(script_dir, "build_comprehensive_catalog.py")
if os.path.exists(build_script):
    import runpy
    runpy.run_path(build_script)
else:
    print("build_comprehensive_catalog.py not found.")
