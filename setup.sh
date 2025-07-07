#!/bin/bash
# Nicaragua Schools Data Project - Setup Script
# This script sets up the project environment and installs dependencies

echo "🇳🇮 Nicaragua Schools Data Project Setup"
echo "========================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if R is installed (optional)
if ! command -v R &> /dev/null; then
    echo "⚠️  R is not installed. R analysis scripts will not work."
    echo "   Install R from https://cran.r-project.org/ to use R features."
else
    echo "✅ R found: $(R --version | head -n1)"
fi

# Check if Chrome is installed
if ! command -v google-chrome &> /dev/null && ! command -v chromium-browser &> /dev/null; then
    echo "⚠️  Chrome browser not found. The scraper requires Chrome."
    echo "   Please install Google Chrome or Chromium."
fi

echo ""
echo "📦 Installing Python dependencies..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

echo "✅ Python dependencies installed!"

# Install R packages if R is available
if command -v R &> /dev/null; then
    echo ""
    echo "📊 Installing R packages..."
    
    cat > install_r_packages.R << 'EOF'
# Read R requirements and install packages
packages <- readLines("r_requirements.txt")
packages <- packages[!grepl("^#", packages) & packages != ""]
packages <- gsub(" >=.*", "", packages)
packages <- packages[packages != ""]

for (pkg in packages) {
  if (!require(pkg, character.only = TRUE, quietly = TRUE)) {
    cat("Installing", pkg, "...\n")
    install.packages(pkg, dependencies = TRUE, repos = "https://cran.r-project.org")
  } else {
    cat("✓", pkg, "already installed\n")
  }
}

cat("R packages installation complete!\n")
EOF
    
    Rscript install_r_packages.R
    rm install_r_packages.R
    
    echo "✅ R packages installed!"
fi

echo ""
echo "🏗️  Creating project structure..."

# Ensure all directories exist
mkdir -p data/raw data/processed data/outputs
mkdir -p scripts/python scripts/r
mkdir -p docs/analysis_reports
mkdir -p src/scrapers src/processors src/analyzers

echo "✅ Project structure created!"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the scraper: python scripts/python/nicaragua_schools_scraper.py"
echo "3. Process data: python scripts/python/data_processing.py"
echo "4. Run R analysis: Rscript scripts/r/exploratory_analysis.R"
echo ""
echo "For more information, see README.md"
