# Exploratory Data Analysis of Nicaragua Schools
# Author: Nicaragua Schools Data Project
# Date: July 2025

# Load required libraries
library(tidyverse)
library(sf)
library(leaflet)
library(plotly)
library(DT)

# Set up paths and configuration
data_path <- here::here("data")
output_path <- here::here("data", "outputs")

# Ensure output directory exists
if (!dir.exists(output_path)) {
  dir.create(output_path, recursive = TRUE)
}

# Function to load the latest Nicaragua schools dataset
load_schools_data <- function() {
  # Look for the most recent complete dataset
  csv_files <- list.files(data_path, pattern = "nicaraguan_schools.*\\.csv$", full.names = TRUE)
  
  if (length(csv_files) == 0) {
    stop("No Nicaragua schools CSV files found in data directory")
  }
  
  # Get the most recent file
  latest_file <- csv_files[which.max(file.mtime(csv_files))]
  
  cat("Loading data from:", basename(latest_file), "\n")
  
  # Read the data
  schools <- read_csv(latest_file, locale = locale(encoding = "UTF-8"))
  
  return(schools)
}

# Load the data
schools_data <- load_schools_data()

# Basic data exploration
cat("=== NICARAGUA SCHOOLS DATASET OVERVIEW ===\n")
cat("Dataset dimensions:", nrow(schools_data), "schools x", ncol(schools_data), "variables\n")
cat("Data collection date: July 2025\n\n")

# Display structure
cat("=== DATASET STRUCTURE ===\n")
str(schools_data)

# Summary statistics
cat("\n=== SUMMARY STATISTICS ===\n")
summary(schools_data)

# Check for missing values
cat("\n=== MISSING VALUES ANALYSIS ===\n")
missing_summary <- schools_data %>%
  summarise_all(~sum(is.na(.))) %>%
  gather(variable, missing_count) %>%
  mutate(missing_percentage = round(missing_count / nrow(schools_data) * 100, 2)) %>%
  arrange(desc(missing_count))

print(missing_summary)

# Geographic distribution by department
cat("\n=== SCHOOLS BY DEPARTMENT ===\n")
department_summary <- schools_data %>%
  count(Department, sort = TRUE) %>%
  mutate(percentage = round(n / sum(n) * 100, 2))

print(department_summary)

# Top municipalities by school count
cat("\n=== TOP 15 MUNICIPALITIES BY SCHOOL COUNT ===\n")
municipality_summary <- schools_data %>%
  count(Department, Municipality, sort = TRUE) %>%
  head(15)

print(municipality_summary)

# Educational modalities analysis
cat("\n=== EDUCATIONAL MODALITIES ANALYSIS ===\n")

# Function to extract and count modalities
extract_modalities <- function(modalidades_col) {
  # Split by common separators and clean
  all_modalities <- schools_data %>%
    filter(!is.na(modalidades_col)) %>%
    pull(modalidades_col) %>%
    str_split("[,;\\|]") %>%
    unlist() %>%
    str_trim() %>%
    str_to_title() %>%
    .[. != ""]
  
  # Count frequency
  modality_counts <- table(all_modalities) %>%
    as.data.frame() %>%
    arrange(desc(Freq)) %>%
    setNames(c("Modality", "Count"))
  
  return(modality_counts)
}

if ("Modalidades" %in% names(schools_data)) {
  modalities_summary <- extract_modalities(schools_data$Modalidades)
  print(head(modalities_summary, 10))
}

# Coordinate quality check
cat("\n=== COORDINATE QUALITY CHECK ===\n")
if (all(c("Latitud", "Longitud") %in% names(schools_data))) {
  coord_summary <- schools_data %>%
    summarise(
      valid_coordinates = sum(!is.na(Latitud) & !is.na(Longitud)),
      missing_coordinates = sum(is.na(Latitud) | is.na(Longitud)),
      lat_range = paste(round(range(Latitud, na.rm = TRUE), 4), collapse = " to "),
      lng_range = paste(round(range(Longitud, na.rm = TRUE), 4), collapse = " to ")
    )
  
  print(coord_summary)
  
  # Check for coordinates outside Nicaragua's approximate bounds
  nicaragua_bounds <- list(
    lat_min = 10.5, lat_max = 15.2,
    lng_min = -87.9, lng_max = -82.6
  )
  
  out_of_bounds <- schools_data %>%
    filter(
      !is.na(Latitud) & !is.na(Longitud) &
      (Latitud < nicaragua_bounds$lat_min | Latitud > nicaragua_bounds$lat_max |
       Longitud < nicaragua_bounds$lng_min | Longitud > nicaragua_bounds$lng_max)
    )
  
  cat("Schools with coordinates outside Nicaragua bounds:", nrow(out_of_bounds), "\n")
}

# Export summary for further analysis
summary_export <- list(
  dataset_info = list(
    total_schools = nrow(schools_data),
    total_departments = n_distinct(schools_data$Department),
    total_municipalities = n_distinct(paste(schools_data$Department, schools_data$Municipality)),
    analysis_date = Sys.Date()
  ),
  department_distribution = department_summary,
  top_municipalities = municipality_summary,
  missing_values = missing_summary
)

# Save summary as RDS for other R scripts
saveRDS(summary_export, file.path(output_path, "exploratory_summary.rds"))

# Save cleaned data for analysis
write_csv(schools_data, file.path(output_path, "nicaragua_schools_clean.csv"))

cat("\n=== ANALYSIS COMPLETE ===\n")
cat("Summary data saved to:", file.path(output_path, "exploratory_summary.rds"), "\n")
cat("Cleaned dataset saved to:", file.path(output_path, "nicaragua_schools_clean.csv"), "\n")
cat("\nNext steps:\n")
cat("- Run spatial_analysis.R for geographic insights\n")
cat("- Run visualizations.R for charts and maps\n")
cat("- Check the outputs folder for results\n")
