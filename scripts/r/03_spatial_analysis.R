# Spatial Analysis of Nicaragua Schools
# Author: Rony Rodriguez
# Date: July 2025

# Load required libraries
library(tidyverse)
library(sf)
library(leaflet)
library(plotly)

# Set up paths
data_path   <- here::here("data", "processed")
output_path <- here::here("data", "outputs")

# Load cleaned data from exploratory analysis
schools_data <- read_csv(file.path(data_path, "nicaragua_schools_clean.csv"))

# Filter schools with valid coordinates
schools_spatial <- schools_data %>%
  filter(!is.na(long) & !is.na(lat)) %>%
  # Convert to sf spatial object
  st_as_sf(coords = c("long", "lat"), crs = 4326)

# Department-level spatial summary
department_spatial <- schools_spatial %>%
  st_drop_geometry() %>%
  group_by(department) %>%
  summarise(
    school_count = n(),
    avg_lat = mean(st_coordinates(schools_spatial)[schools_spatial$department == department[1], "Y"]),
    avg_lng = mean(st_coordinates(schools_spatial)[schools_spatial$department == department[1], "X"]),
    .groups = "drop"
  )

# School density analysis by municipality
municipality_density <- schools_spatial %>%
  st_drop_geometry() %>%
  group_by(department, municipality) %>%
  summarise(
    school_count = n(),
    avg_lat = mean(st_coordinates(schools_spatial)[schools_spatial$municipality == municipality[1], "Y"]),
    avg_lng = mean(st_coordinates(schools_spatial)[schools_spatial$municipality == municipality[1], "X"]),
    .groups = "drop"
  ) %>%
  arrange(desc(school_count))

# Maps of Schools by Department
leaflet(department_spatial) %>%
  addTiles() %>%
  addCircleMarkers(
    lng = ~avg_lng, 
    lat = ~avg_lat, 
    radius = ~sqrt(school_count) * 2, 
    popup = ~paste0(department, ": ", school_count, " schools"),
    color = "blue",
    fillOpacity = 0.5
  ) %>%
  setView(lng = -85.2072, lat = 12.8654, zoom = 6) %>%
  addLegend("bottomright", pal = colorNumeric("Blues", NULL), values = department_spatial$school_count, title = "Number of Schools")

# Maps of Schools by Municipality
leaflet(municipality_density) %>%
  addTiles() %>%
  addCircleMarkers(
    lng = ~avg_lng, 
    lat = ~avg_lat, 
    radius = ~sqrt(school_count) * 2, 
    popup = ~paste0(municipality, ": ", school_count, " schools"),
    color = "red",
    fillOpacity = 0.5
  ) %>%
  setView(lng = -85.2072, lat = 12.8654, zoom = 7) %>%
  addLegend("bottomright", pal = colorNumeric("Reds", NULL), values = municipality_density$school_count, title = "Number of Schools")
