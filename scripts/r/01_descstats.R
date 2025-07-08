# Cleaning and Descriptive Analysis
# Author: Rony Rodriguez
# Date: July 2025

# Load required libraries
library(tidyverse)

# Set up paths and configuration
data_path <- here::here("data")
output_path <- here::here("data", "outputs")
raw_path <- here::here("data", "raw")

# Ensure output directory exists
if (!dir.exists(output_path)) {
  dir.create(output_path, recursive = TRUE)
}

# Load the data
schools_data <- read_csv(file.path(raw_path, "nicaraguan_schools_250708.csv"))

# Calculate the max number of new columns needed for program_labels
max_labels <- schools_data %>%
  mutate(
    program_labels_upper = str_to_upper(program_labels),
    labels_list = str_split(program_labels_upper, ",\\s*")
  ) %>%
  pull(labels_list) %>%
  map_int(length) %>%
  max(na.rm = TRUE)

max_modalities <- schools_data %>%
  mutate(
    modality_labels_upper = str_to_upper(modality_labels),
    modalities_list = str_split(modality_labels_upper, ",\\s*")
  ) %>%
  pull(modalities_list) %>%
  map_int(length) %>%
  max(na.rm = TRUE)

new_names <- str_c("program_labels_", 1:max_labels)
new_modality_names <- str_c("modality_labels_", 1:max_modalities)

schools_data <- schools_data %>%
  bind_cols(
    separate(
      .,
      col = program_labels,
      into = new_names,
      sep = ",\\s*",
      fill = "right",
      remove = FALSE
    ) %>%
      select(all_of(new_names))
  ) %>%
  bind_cols(
    separate(
      .,
      col = modality_labels,
      into = new_modality_names,
      sep = ",\\s*",
      fill = "right",
      remove = FALSE
    ) %>%
      select(all_of(new_modality_names))
  )

schools_data <- schools_data %>%
  janitor::clean_names() %>%
  select(
    department,
    dep_id,
    municipality,
    mun_id,
    school_id,
    school_name = nombre,
    lat = latitud,
    long = longitud,
    address = direccion,
    program_ids,
    program_labels,
    starts_with("program_labels_"),
    modality_ids,
    modality_labels,
    starts_with("modality_labels_")
  )
