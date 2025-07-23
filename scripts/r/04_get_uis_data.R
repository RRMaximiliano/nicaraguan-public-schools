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
  # count(indicator_name) %>% View()
  filter(indicator_name == "Pupil-trained teacher ratio in secondary education (headcount basis)") %>% 
  ggplot(aes(x = as.numeric(year), y = value, color = entity_id, group = entity_id)) +
  geom_line(linewidth = 1) +
  facet_wrap(~entity_id) +
  labs(
    x = NULL,
    y = "Pupil-trained teacher ratio in secondary education (headcount basis)",
    title = "Pupil-trained Teacher Ratio in Secondary Education",
    subtitle = "Nicaragua and Central America (1990-2024)",
    caption = "Source: UNESCO Institute for Statistics (UIS) ⋅ Plot: @rrmaximiliano"
  ) +
  theme_ipsum_es() +
  theme(
    legend.position = "none",
    plot.title = element_text(hjust = 0, size = 16, face = "bold"),
    plot.subtitle = element_text(hjust = 0, size = 14)
  )

ggsave(file.path(output_path, "figs/pupil_trained_teacher_ratio_ca.png"), width = 10, height = 6, dpi = 300, bg = "white")
