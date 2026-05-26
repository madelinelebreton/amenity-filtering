import osmium
import geopandas as gpd
from shapely.geometry import Point, LineString
from pathlib import Path
import yaml
import sys

# -----------------------------
# Load config
# -----------------------------
config_path = sys.argv[1] if len(sys.argv) > 1 else "config.yaml"

with open(config_path, "r") as f:
    config = yaml.safe_load(f)

BASE = Path(__file__).resolve().parents[1]

osm_data = BASE / config["paths"]["osm_data"]
output_dir = BASE / config["paths"]["outputs"]
output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / "osm_filtered.gpkg"

# -----------------------------
# Filters
# -----------------------------
ALLOWED_TOURISM = {
    "restaurant",
    "museum",
    "attraction",
    "gallery",
    "zoo",
    "viewpoint",
    "theme_park"
}

ALLOWED_HIGHWAYS = {
    "motorway",
    "trunk",
    "primary",
    "secondary",
    "tertiary",
    "unclassified"
}

features = []

class OSMHandler(osmium.SimpleHandler):

    # ------------------------
    # POINTS OF INTEREST
    # ------------------------
    def node(self, n):

        # tourism / POIs
        if 'tourism' in n.tags:
            if n.tags['tourism'] in ALLOWED_TOURISM:

                try:
                    features.append({
                        'type': 'poi',
                        'class': n.tags['tourism'],
                        'name': n.tags.get('name'),
                        'geometry': Point(n.location.lon, n.location.lat)
                    })
                except:
                    pass

        # restaurants are usually amenity
        if 'amenity' in n.tags:
            if n.tags['amenity'] == 'restaurant':

                try:
                    features.append({
                        'type': 'poi',
                        'class': 'restaurant',
                        'name': n.tags.get('name'),
                        'geometry': Point(n.location.lon, n.location.lat)
                    })
                except:
                    pass

    # ------------------------
    # ROADS
    # ------------------------
    def way(self, w):

        if 'highway' in w.tags:

            if w.tags['highway'] in ALLOWED_HIGHWAYS:

                try:
                    coords = [(n.lon, n.lat) for n in w.nodes]
                    if len(coords) > 1:

                        features.append({
                            'type': 'road',
                            'class': w.tags['highway'],
                            'name': w.tags.get('name'),
                            'geometry': LineString(coords)
                        })

                except:
                    pass

# -----------------------------
# Run extraction
# -----------------------------
handler = OSMHandler()

handler.apply_file(
    str(osm_data),
    locations=True
)

gdf = gpd.GeoDataFrame(features, crs="EPSG:4326")
gdf.to_file(output_path, driver="GPKG")

print("Roads and POIs saved to:", output_path)