library(r5r)
library(sf)
library(data.table)
library(smoothr)
library(rJava)
library(yaml)

# -----------------------------
# Load config
# -----------------------------
args <- commandArgs(trailingOnly = TRUE)
config <- yaml::read_yaml(args[1])

data_path <- config$paths$osm_folder

# -----------------------------
# Extract config values
# -----------------------------
lat <- config$origin$lat
lon <- config$origin$lon

cutoffs <- config$isochrones$cutoffs
mode <- config$isochrones$mode
time_window <- config$isochrones$time_window

departure_datetime <- as.POSIXct(
  config$isochrones$departure_datetime,
  format = "%Y-%m-%d %H:%M:%S"
)

# -----------------------------
# Paths
# -----------------------------
output_dir <- config$paths$outputs

# -----------------------------
# Build network
# -----------------------------
options(java.parameters = "-Xmx6G")

r5r_network <- build_network(data_path, verbose = TRUE)

street_net <- street_network_to_sf(r5r_network)

allowed_roads <- c(
  "MOTORWAY",
  "TRUNK",
  "PRIMARY",
  "SECONDARY",
  "TERTIARY",
  "UNCLASSIFIED"
)

main_roads <- subset(
  street_net$edges,
  street_class %in% allowed_roads
)

# -----------------------------
# Origin
# -----------------------------
origins <- data.table(
  id = "origin_1",
  lat = lat,
  lon = lon
)

# -----------------------------
# Isochrone computation
# -----------------------------
iso <- isochrone(
  r5r_network,
  origins = origins,
  mode = c(mode),
  cutoffs = cutoffs,
  departure_datetime = departure_datetime,
  max_trip_duration = max(cutoffs),
  time_window = time_window,
  polygon_output = TRUE,
  progress = TRUE
)

iso <- smooth(iso, method = "chaikin")

iso <- st_transform(iso, 3857)
main_roads <- st_transform(main_roads, 3857)

# -----------------------------
# Save outputs
# -----------------------------
st_write(
  iso,
  file.path(output_dir, "isochrones.gpkg"),
  layer = "isochrones",
  delete_dsn = TRUE
)


r5r::stop_r5(r5r_network)
rJava::.jgc(R.gc = TRUE)

print("Isochrones complete")