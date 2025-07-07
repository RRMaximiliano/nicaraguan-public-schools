# Contributing to Nicaragua Schools Data Project

Thank you for your interest in contributing to the Nicaragua Schools Data Project. This document provides guidelines for contributing to the project, though we recognize that guidelines can sometimes be more prescriptive than helpful, so feel free to reach out if something doesn't make sense.

## Ways to Contribute

### Data Collection and Quality

- Improve web scraping efficiency and reliability
- Enhance data validation and cleaning processes
- Add new data sources or fields
- Report data quality issues or inconsistencies

### Analysis and Visualization

- Create new analytical insights and visualizations
- Improve existing R and Python analysis scripts
- Add statistical models or machine learning approaches
- Develop interactive dashboards or reports

### Documentation and Code Quality

- Improve code documentation and comments
- Update README and technical documentation
- Add examples and tutorials
- Translate documentation to Spanish

### Technical Improvements

- Optimize performance and memory usage
- Add error handling and logging
- Implement automated testing
- Improve project structure and organization

## Development Setup

1. **Fork the repository** on GitHub

2. **Clone your fork**:

   ```bash
   git clone https://github.com/yourusername/nicaraguan-public-schools.git
   cd nicaraguan-public-schools
   ```

3. **Run the setup script**:

   ```bash
   ./setup.sh
   ```

4. **Create a feature branch**:

   ```bash
   git checkout -b feature/your-feature-name
   ```

## 📝 Code Guidelines

### Python Code Standards
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Include docstrings for all functions and classes
- Add type hints where appropriate
- Include error handling for external dependencies

Example:
```python
def validate_coordinates(lat: float, lng: float) -> Tuple[bool, str]:
    """
    Validate if coordinates are within Nicaragua's boundaries.
    
    Args:
        lat: Latitude coordinate
        lng: Longitude coordinate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Implementation here
```

### R Code Standards
- Follow tidyverse style conventions
- Use descriptive variable names (snake_case)
- Include comments explaining complex operations
- Use meaningful plot titles and labels
- Structure scripts with clear sections

Example:
```r
# Load and clean school data
schools_clean <- schools_raw %>%
  filter(!is.na(latitud) & !is.na(longitud)) %>%
  mutate(department_clean = str_to_title(department))
```

### Git Commit Guidelines
- Use clear, descriptive commit messages
- Start with a verb in present tense
- Keep the first line under 50 characters
- Include detailed description if needed

Examples:
```
Add coordinate validation function
Fix department name standardization
Update README with new analysis features
```

## 🧪 Testing

### Python Testing
- Add unit tests for new functions
- Test with sample data from different departments
- Verify error handling for edge cases
- Run existing tests: `python -m pytest`

### R Testing
- Test scripts with different data subsets
- Verify plot generation and outputs
- Check for missing value handling
- Test on different operating systems

### Data Quality Testing
- Validate output data format and completeness
- Check coordinate boundaries and consistency
- Verify school code formats
- Test with historical data

## 📊 Data Contribution Guidelines

### New Data Sources
- Document the data source and collection method
- Ensure data is publicly available
- Include data quality assessment
- Provide mapping to existing schema

### Data Processing
- Maintain backward compatibility
- Document any schema changes
- Include data validation steps
- Preserve raw data integrity

## 🔍 Pull Request Process

1. **Ensure your code follows the style guidelines**
2. **Add or update tests** for your changes
3. **Update documentation** as needed
4. **Create a descriptive pull request**:
   - Clear title summarizing the change
   - Detailed description of what was changed and why
   - Reference any related issues
   - Include screenshots for visualization changes

5. **Respond to feedback** and make requested changes
6. **Ensure all checks pass** before requesting final review

## 📋 Issue Reporting

### Bug Reports
Include:
- Operating system and Python/R versions
- Steps to reproduce the issue
- Expected vs actual behavior
- Error messages or screenshots
- Sample data (if relevant)

### Feature Requests
Include:
- Clear description of the proposed feature
- Use case and benefits
- Implementation suggestions
- Potential challenges or considerations

### Data Issues
Include:
- Specific department/municipality affected
- Description of the data problem
- Screenshots or data samples
- Suggested corrections

## 🌍 Internationalization

We welcome contributions in both English and Spanish:

- **English**: Primary language for code and technical documentation
- **Spanish**: Welcome for user-facing content, analysis reports, and documentation
- **Bilingual**: Ideal for README sections and user guides

## 📞 Communication

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Pull Requests**: For code contributions and documentation

## 🎖️ Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- Academic publications using this data (with permission)

## 📄 License

By contributing, you agree that your contributions will be licensed under the same MIT License that covers the project.

## 🤝 Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please be respectful in all interactions and help us maintain a positive environment for everyone.

---

Thank you for contributing to improving educational data accessibility in Nicaragua! 🇳🇮
