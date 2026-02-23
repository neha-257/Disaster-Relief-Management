# Frontend Folder Organization

This folder contains the frontend files for the Disaster Relief Management system, based on the BootstrapMade Avilon template.

## Folder Structure

- **css/**: Contains the project's main CSS files
  - main.css: Primary stylesheet for the application
  
- **js/**: Contains the project's JavaScript files
  - main.js: Main JavaScript functionality for the application
  
- **assets/**: Contains vendor libraries, images, fonts, and other resources
  - img/: Image files
  - vendor/: Third-party libraries (Bootstrap, AOS, etc.)
  - scss/: SCSS source files (if applicable)
  
- **templates/**: Template HTML files
  
- **forms/**: Form processing files

## File Organization Notes

The template-specific CSS and JavaScript files have been moved from assets/css/main.css and assets/js/main.js to the frontend/css/ and frontend/js/ folders respectively, while keeping the assets folder for fonts, images, and vendor libraries.

All HTML files reference these new locations to maintain the same functionality as before. 