library(sf)
library(yaml)

config <- yaml::read_yaml("config.yaml")
RSCRIPT = config["r"]["rscript_path"]

output_dir <- normalizePath(config$paths$outputs)

borders <- st_read(file.path(output_dir, "national_borders.gpkg"))

osm_filtered <- st_read(file.path(output_dir, "osm_filtered.gpkg"))

iso <- st_read(file.path(output_dir, "isochrones.gpkg"))

final_file <- file.path(output_dir, paste0(config$project$name, ".gpkg"))

# overwrite cleanly
if (file.exists(final_file)) file.remove(final_file)

st_write(borders, final_file, layer = "borders")
st_write(osm_filtered, final_file, layer = "roads", append = TRUE)
st_write(iso, final_file, layer = "isochrones", append = TRUE)

print(paste("Final GeoPackage:", final_file))

print(paste("Final GeoPackage:", final_file))