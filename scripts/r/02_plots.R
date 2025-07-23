# Visualizations for Nicaragua Schools Data
# Author: Rony Rodriguez
# Date: July 2025

# Load required libraries
library(tidyverse)
library(stringi)
library(hrbrthemes)
library(ggtext)

# Set up paths
data_path   <- here::here("data")
output_path <- here::here("outputs")

# Load data
schools_data <- read_csv(file.path(data_path, "processed/nicaragua_schools_clean.csv")) %>% 
  # Remove accents in strings: department and municipality
  mutate(
    across(
      .cols = c(department, municipality),
      .fns  = ~ stri_trans_general(., "Latin-ASCII")
    )
  )  
  
# Schools by Department 
schools_data %>% 
  count(department) %>% 
  ggplot(
    aes(
      x = n, 
      y = reorder(department, n)
    )
  ) +
  geom_col(color = "black", fill = "grey", width = 0.6) +
  geom_text(
    aes(label = format(n, big.mark = ",", scientific = FALSE)), 
    hjust = -0.2, 
    size = 3.5, 
    color = "black",
    family = "Econ Sans Cnd"
  ) + 
  coord_cartesian(clip = "off") +
  labs(
    title = "Number of Schools by Department",
    subtitle = "Nicaragua Educational Infrastructure",
    y = NULL,
    x = "Number of Schools",
    caption = "**Source**: Nicaragua Ministry of Education ⋅ **Plot**: @rrmaximiliano"
  ) + 
  theme_ipsum_es() +
  theme(
    panel.grid.minor.x = element_blank(),
    plot.caption = element_markdown(),
  )

# Save the plot
ggsave(file.path(output_path, "figs/schools_by_department.png"), width = 10, height = 6, dpi = 300, bg = "white")

# Schools by Municipalities, Top 15
schools_data %>% 
  count(municipality) %>% 
  top_n(15, n) %>% 
  ggplot(
    aes(
      x = n, 
      y = reorder(municipality, n)
    )
  ) +
  geom_col(color = "black", fill = "grey", width = 0.6) +
  geom_text(
    aes(label = format(n, big.mark = ",", scientific = FALSE)), 
    hjust = -0.2, 
    size = 3.5, 
    color = "black",
    family = "Econ Sans Cnd"
  ) + 
  coord_cartesian(clip = "off") +
  labs(
    title = "Top 15 Municipalities by Number of Schools",
    subtitle = "Nicaragua Educational Infrastructure",
    y = NULL,
    x = "Number of Schools",
    caption = "**Source**: Nicaragua Ministry of Education ⋅ **Plot**: @rrmaximiliano"
  ) + 
  theme_ipsum_es() +
  theme(
    panel.grid.minor.x = element_blank(),
    plot.caption = element_markdown(),
  )

ggsave(file.path(output_path, "figs/schools_by_municipality.png"), width = 10, height = 6, dpi = 300, bg = "white")


# Schools by Modality
modality_counts <- schools_data %>% 
  select(-c(modality_labels_1:modality_labels_10)) %>% 
  separate_rows(modality_labels, sep = ",") %>%
  # count how many schools have each modality
  count(modality = modality_labels) %>%
  arrange(desc(n))

# Select top N modalities (e.g. top 10)
top_modality_counts <- modality_counts %>%
  slice_head(n = 10)

# Plot horizontal bar chart
top_modality_counts %>% 
  ggplot(
    aes(
      x = n, 
      y = reorder(modality, n)
    )
  ) +
  geom_col(color = "black", fill = "grey", width = 0.6) +
  geom_text(
    aes(label = format(n, big.mark = ",", scientific = FALSE)), 
    hjust = -0.2, 
    size = 3.5, 
    color = "black",
    family = "Econ Sans Cnd"
  ) +
  coord_cartesian(clip = "off") +
  labs(
    title = "Top 10 School Modalities in Nicaragua",
    subtitle = "Diverse Educational Offerings",
    y = NULL,
    x = "Number of Schools",
    caption = "**Source**: Nicaragua Ministry of Education ⋅ **Plot**: @rrmaximiliano"
  ) +
  theme_ipsum_es() +
  theme(
    panel.grid.minor.x = element_blank(),
    plot.caption = element_markdown(),
  )

ggsave(file.path(output_path, "figs/schools_by_modality.png"), width = 10, height = 6, dpi = 300, bg = "white")
