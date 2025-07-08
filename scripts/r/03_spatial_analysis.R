# Spatial Analysis of Nicaragua Schools
# Author: Rony Rodriguez
# Date: July 2025

# Load required libraries
library(tidyverse)
library(sf)
library(leaflet)
library(plotly)

# Set up paths
data_path <- here::here("data", "outputs")
output_path <- here::here("data", "outputs")

# Load cleaned data from exploratory analysis
schools_data <- read_csv(file.path(data_path, "nicaragua_schools_clean.csv"))

# Create spatial data
cat("=== CREATING SPATIAL DATA ===\n")

# Filter schools with valid coordinates
schools_spatial <- schools_data %>%
  filter(!is.na(Latitud) & !is.na(Longitud)) %>%
  # Convert to sf spatial object
  st_as_sf(coords = c("Longitud", "Latitud"), crs = 4326)

cat("Created spatial data for", nrow(schools_spatial), "schools with valid coordinates\n")

# Department-level spatial summary
department_spatial <- schools_spatial %>%
  st_drop_geometry() %>%
  group_by(Department) %>%
  summarise(
    school_count = n(),
    avg_lat = mean(st_coordinates(schools_spatial)[schools_spatial$Department == Department[1], "Y"]),
    avg_lng = mean(st_coordinates(schools_spatial)[schools_spatial$Department == Department[1], "X"]),
    .groups = "drop"
  )

# School density analysis by municipality
municipality_density <- schools_spatial %>%
  st_drop_geometry() %>%
  group_by(Department, Municipality) %>%
  summarise(
    school_count = n(),
    avg_lat = mean(st_coordinates(schools_spatial)[schools_spatial$Municipality == Municipality[1], "Y"]),
    avg_lng = mean(st_coordinates(schools_spatial)[schools_spatial$Municipality == Municipality[1], "X"]),
    .groups = "drop"
  ) %>%
  arrange(desc(school_count))

# Save spatial summaries
write_csv(department_spatial, file.path(output_path, "department_spatial_summary.csv"))
write_csv(municipality_density, file.path(output_path, "municipality_density.csv"))

cat("Spatial analysis complete. Files saved to outputs directory.\n")
cat("Next: Run visualizations.R to create maps and charts.\n")
