# Visualizations for Nicaragua Schools Data
# Author: Rony Rodriguez
# Date: July 2025

# Load required libraries
library(tidyverse)
library(sf)
library(leaflet)
library(plotly)
library(ggplot2)

# Set up paths
data_path <- here::here("data", "outputs")
output_path <- here::here("data", "outputs")

# Load data
schools_data <- read_csv(file.path(data_path, "nicaragua_schools_clean.csv"))
department_summary <- read_csv(file.path(data_path, "department_spatial_summary.csv"))

cat("=== CREATING VISUALIZATIONS ===\n")

# 1. Schools by Department Bar Chart
dept_plot <- ggplot(department_summary, aes(x = reorder(Department, school_count), y = school_count)) +
  geom_col(fill = "steelblue", alpha = 0.8) +
  coord_flip() +
  labs(
    title = "Number of Schools by Department",
    subtitle = "Nicaragua Educational Infrastructure",
    x = "Department",
    y = "Number of Schools",
    caption = "Source: Nicaragua Ministry of Education"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(size = 14, face = "bold"),
    plot.subtitle = element_text(size = 12),
    axis.text = element_text(size = 10)
  )

# Save the plot
ggsave(file.path(output_path, "schools_by_department.png"), 
       dept_plot, width = 10, height = 6, dpi = 300)

# 2. Interactive Map (basic version)
if (all(c("Latitud", "Longitud") %in% names(schools_data))) {
  # Sample schools for interactive map (to avoid performance issues)
  schools_sample <- schools_data %>%
    filter(!is.na(Latitud) & !is.na(Longitud)) %>%
    sample_n(min(1000, nrow(.)))  # Sample up to 1000 schools
  
  # Create interactive map
  schools_map <- leaflet(schools_sample) %>%
    addTiles() %>%
    addCircleMarkers(
      lng = ~Longitud,
      lat = ~Latitud,
      radius = 3,
      popup = ~paste0(
        "<strong>", Nombre, "</strong><br>",
        "Department: ", Department, "<br>",
        "Municipality: ", Municipality, "<br>",
        "Address: ", Direccion
      ),
      clusterOptions = markerClusterOptions()
    ) %>%
    setView(lng = -85.2, lat = 12.9, zoom = 7)
  
  # Save map as HTML
  htmlwidgets::saveWidget(
    schools_map, 
    file.path(output_path, "nicaragua_schools_map.html"),
    selfcontained = TRUE
  )
}

cat("Visualizations created successfully!\n")
cat("Files saved to:", output_path, "\n")
cat("- schools_by_department.png: Bar chart of schools by department\n")
cat("- nicaragua_schools_map.html: Interactive map of schools\n")
