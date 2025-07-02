#!/usr/bin/env Rscript
# SFigure 3: ArXiv Preprints Over Time
#
# Publication-ready plot showing the growth of arXiv submissions from 1991 to 2025.
# Optimized for single-column format in academic preprints.
# Runs in headless mode by default (no display window).
# Data source: https://arxiv.org/stats/monthly_submissions.
#
# Usage:
#   Rscript SFigure_3.R           # Headless mode (save files only)
#   Rscript SFigure_3.R --show    # Display plot and save files
#   Rscript SFigure_3.R --help    # Show help message

# Function to check and install required packages
check_and_install_packages <- function(packages) {
  for (pkg in packages) {
    if (!require(pkg, character.only = TRUE)) {
      install.packages(pkg, repos = "https://cloud.r-project.org/")
      library(pkg, character.only = TRUE)
    }
  }
}

# List of required packages
required_packages <- c("ggplot2", "scales", "readr", "dplyr", "optparse", "svglite")
check_and_install_packages(required_packages)

# Ensure svglite is loaded
if (!requireNamespace("svglite", quietly = TRUE)) {
  warning("The 'svglite' package is not installed. SVG output may not work.")
} else {
  library(svglite)  # Explicitly load svglite to ensure it is recognized
}

library(ggplot2)
library(scales)
library(readr)
library(dplyr)
library(optparse)

# Parse command-line arguments
option_list <- list(
  make_option(c("--show"), action = "store_true", default = FALSE, help = "Display plot"),
  make_option(c("--help"), action = "store_true", default = FALSE, help = "Show help message")
)
opt <- parse_args(OptionParser(option_list = option_list))

if (opt$help) {
  cat("Usage: Rscript SFigure_3.R [--show] [--help]\n")
  cat("  --show: Display plot (default is headless mode)\n")
  cat("  --help: Show this help message\n")
  quit(status = 0)
}

# Load and process data
load_and_process_data <- function() {
  # Get the directory of the current script
  script_args <- commandArgs(trailingOnly = FALSE)
  script_path <- normalizePath(sub("--file=", "", script_args[grep("--file=", script_args)]))
  script_dir <- dirname(script_path)
  
  # Define the path to the data file
  data_path <- file.path(script_dir, "DATA", "SFigure_3", "arxiv_monthly_submissions.csv")
  
  # Check if the file exists
  if (!file.exists(data_path)) {
    stop(paste("Error: Data file not found at", data_path))
  }
  
  # Load and process the data
  df <- read_csv(data_path)
  df <- df %>%
    mutate(date = as.Date(paste0(month, "-01"), format = "%Y-%m-%d")) %>%
    arrange(date)
  return(df)
}

# Create the figure
create_figure <- function(df) {
  peak <- df %>% filter(submissions == max(submissions))
  peak_label <- paste0("Peak: ", format(peak$submissions / 1000, digits = 1), "k\n(", format(peak$date, "%Y"), ")")
  
  p <- ggplot(df, aes(x = date, y = submissions)) +
    geom_line(color = "#2E86AB", linewidth = 0.6, alpha = 0.8) +  # Updated `size` to `linewidth`
    geom_area(fill = "#2E86AB", alpha = 0.2) +
    labs(
      title = "arXiv Preprint Growth (1991-2025)",
      x = "Year",
      y = "Monthly Submissions"
    ) +
    scale_x_date(
      date_breaks = "10 years",
      date_minor_breaks = "5 years",
      date_labels = "%Y"
    ) +
    scale_y_continuous(
      labels = function(x) ifelse(x >= 1000, paste0(x / 1000, "k"), x),
      expand = expansion(mult = c(0, 0.05))
    ) +
    theme_minimal(base_size = 8) +
    theme(
      axis.title = element_text(face = "bold"),
      plot.title = element_text(face = "bold", size = 10, hjust = 0.5),
      panel.grid.minor = element_line(linewidth = 0.3, linetype = "dotted"),  # Updated `size` to `linewidth`
      panel.grid.major = element_line(linewidth = 0.3),  # Updated `size` to `linewidth`
      axis.text.x = element_text(angle = 0, hjust = 0.5)
    ) +
    annotate(
      "text",
      x = max(df$date),
      y = max(df$submissions),
      label = peak_label,
      hjust = 1.1,
      vjust = 1.1,
      size = 2.5,
      color = "black",
      fontface = "bold"
    )
  return(p)
}

# Save the figure
save_figure <- function(p, output_path = NULL) {
  output_path <- ifelse(is.null(output_path), getwd(), output_path)
  
  # Ensure the output directory exists
  if (!dir.exists(output_path)) {
    dir.create(output_path, recursive = TRUE)
  }
  
  # Save the figure in multiple formats
  ggsave(file.path(output_path, "SFigure_3.pdf"), plot = p, width = 3.5, height = 4, dpi = 300)
  ggsave(file.path(output_path, "SFigure_3.png"), plot = p, width = 3.5, height = 4, dpi = 300)
  
  # Use svglite if available, otherwise fallback to default svg device
  if (requireNamespace("svglite", quietly = TRUE)) {
    ggsave(file.path(output_path, "SFigure_3.svg"), plot = p, width = 3.5, height = 4, device = "svglite")
  } else {
    ggsave(file.path(output_path, "SFigure_3.svg"), plot = p, width = 3.5, height = 4, device = "svg")
  }
  
  cat("Figure saved to:\n")
  cat(paste0("  - ", file.path(output_path, "SFigure_3.pdf"), "\n"))
  cat(paste0("  - ", file.path(output_path, "SFigure_3.png"), "\n"))
  cat(paste0("  - ", file.path(output_path, "SFigure_3.svg"), "\n"))
}

# Main function
main <- function() {
  df <- load_and_process_data()
  p <- create_figure(df)
  save_figure(p)
  if (opt$show) {
    print(p)
  }
}

main()
