<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Nicaragua Schools Scraper Project Instructions

This project is a Python web scraping application that extracts school data from Nicaragua's Ministry of Education website using Selenium WebDriver.

## Project Context
- **Purpose**: Scrape comprehensive school data from all departments and municipalities in Nicaragua
- **Technology**: Python with Selenium WebDriver, Chrome browser automation
- **Data Source**: Nicaragua Ministry of Education's online education map
- **Output**: CSV file with school details including location, codes, names, addresses, and modalities

## Key Implementation Details
- Uses fresh Chrome browser instances for each municipality to avoid caching issues
- Implements proper error handling and timeout management
- Extracts data from JavaScript-rendered Leaflet map markers
- Processes HTML content with regex patterns for school information
- Includes comprehensive Chrome options for reliable automation

## Code Style Guidelines
- Follow PEP 8 Python style guidelines
- Use descriptive variable names and functions
- Include comprehensive error handling with try-catch blocks
- Add informative logging and progress indicators
- Implement proper resource cleanup (context managers)

## Testing Considerations
- Test with different Chrome browser versions
- Verify data extraction accuracy across municipalities
- Handle network timeouts and connection issues
- Validate CSV output format and encoding

## Performance Optimization
- Implement delays between requests to be respectful to the server
- Use efficient data structures for large datasets
- Optimize Chrome options for faster page loading
- Consider parallel processing for different departments (if needed)

## Dependencies
- selenium: Web automation
- pandas: Data manipulation and CSV export
- chromedriver-autoinstaller: Chrome driver management
- Standard library: re, html, time for data processing
