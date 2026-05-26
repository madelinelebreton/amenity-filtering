# run_pipeline.py
# purpose: executes configured files sequentially to build QGIS file
# author: madeline lebreton
# date: 26.05.2026

import subprocess
from pathlib import Path
import yaml

BASE = Path(__file__).parent
CONFIG_PATH = BASE / "config.yaml"

print("RUNNING FROM:", BASE)
print("CONFIG PATH:", CONFIG_PATH)

# -----------------------------
# Load config file
# -----------------------------
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)
    
# -----------------------------
# Extract values
# -----------------------------
RSCRIPT = config.get("r", {}).get("rscript_path", "Rscript")

print("Using Rscript:", RSCRIPT)

print("Starting accessibility pipeline")

# -----------------------------
# 1. OSM extraction (Python)
# -----------------------------
subprocess.run([
    "python",
    BASE / "scripts/extract_osm.py",
    str(CONFIG_PATH)
], check=True)

print("OSM data extracting finished")
# -----------------------------
# 2. Isochrones (R)
# -----------------------------
subprocess.run([
    RSCRIPT,
    BASE / "scripts/run_isochrones.R",
    str(CONFIG_PATH)
], check=True)
print("Isochrone mapping finished")

# -----------------------------
# 3. Draw borders (R)
# -----------------------------
subprocess.run([
    RSCRIPT,
    BASE / "scripts/draw_borders.R",
    str(CONFIG_PATH)
], check=True)
print("Draw borders finished")

# -----------------------------
# 4. Merge outputs (R)
# -----------------------------
subprocess.run([
    RSCRIPT,
    BASE / "scripts/merge_outputs.R",
    str(CONFIG_PATH)
], check=True)
print("Merge outputs finished")


print("Pipeline complete — QGIS output created")