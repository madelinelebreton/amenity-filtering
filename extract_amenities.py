import osmium
import geopandas as gpd
from shapely.geometry import Point

# ensure path is desired working directory
from pathlib import Path

BASE = Path(r"C:\Users\Equipo\Documents\ss_ML_local\ammenity-filtering-github")



features = []

class AmenityHandler(osmium.SimpleHandler):

    def node(self, n):

        if 'amenity' in n.tags:

            try:
                features.append({
                    'amenity': n.tags['amenity'],
                    'name': n.tags.get('name'),
                    'geometry': Point(n.location.lon, n.location.lat)
                })

            except:
                pass


handler = AmenityHandler()

handler.apply_file(
    r"georgia-260518.osm.pbf",
    locations=True
)

gdf = gpd.GeoDataFrame(
    features,
    crs="EPSG:4326"
)

gdf.to_file(
    r"C:\Users\Equipo\Documents\ss_ML_local\Python\amenities.gpkg",
    driver="GPKG"
)

print(gdf.head())
print(f"Extracted {len(gdf)} amenities")

