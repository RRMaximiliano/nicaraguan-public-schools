# UNESCO UIS Data Integration for Nicaragua Schools
# Author: Rony Rodriguez  
# Date: July 2025

# Packages ---------------------------------------------------------------

library(tidyverse)
library(uisapi)

# Get Data ---------------------------------------------------------------

# uis_get_entities()
# uis_get_versions()

teacher_indicators <- uis_get_indicators() %>% 
  filter(str_detect(indicator_name, "teacher"))

teacher_vector <- teacher_indicators %>% 
  pull(indicator_id)

nicaragua_teachers <- uis_get(
  entities = c("BLZ", "CRI", "SLV", "GTM", "HND", "NIC", "PAN"), 
  indicators = teacher_vector,
  start_year = 1990,
  end_year = 2024
) %>% 
  left_join(teacher_indicators %>% select(indicator_name,indicator_id), by = "indicator_id")

# To wide format
nicaragua_teachers %>% 
  pivot_wider(
    names_from = indicator_id,
    values_from = value
  )


# dt <- read_csv("nicaraguan_schools_all.csv")  

# dt %>% 
#   count(municipality) %>% View()
