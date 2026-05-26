library(geodata)
library(sf)
library(terra)
library(yaml)

# QGIS passes args differently than subprocess scripts
args <- commandArgs(trailingOnly = TRUE)
config <- yaml::read_yaml(args[1])

country_codes <- trimws(strsplit(config$project$countries, ",")[[1]])

list_of_countries <- lapply(country_codes, function(code) {
  x <- geodata::gadm(country = code, level = 0, path = tempdir())
  st_as_sf(x)
})

National_borders <- do.call(rbind, list_of_countries)
National_borders <- st_make_valid(National_borders)

# 🔥 CRITICAL FIX: ensure output directory exists
out_file <- file.path(config$paths$outputs, "national_borders.gpkg")
dir.create(dirname(out_file), recursive = TRUE, showWarnings = FALSE)

# overwrite safely
sf::st_write(National_borders, out_file, delete_dsn = TRUE)