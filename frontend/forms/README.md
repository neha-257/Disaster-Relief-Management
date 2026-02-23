# Form Processing System

This directory contains PHP scripts that handle form submissions from the Disaster Relief Management System's frontend. These are placeholder implementations that simulate successful responses but don't perform actual database operations.

## Available Form Handlers

- **contact.php** - Processes contact form submissions from the Contact Us page
- **victim-add.php** - Handles victim registration form submissions
- **missing-report.php** - Processes missing person report submissions
- **volunteer-register.php** - Handles volunteer registration form submissions
- **donation.php** - Processes donation form submissions
- **supply-update.php** - Handles inventory/supply update operations

## Implementation Notes

- These are placeholder implementations for demonstration purposes
- In a production environment, these would connect to an actual database
- All form handlers validate input data before processing
- Responses are returned as JSON for easy integration with frontend JavaScript

## How to Use

1. Configure your web server to support PHP
2. Update the database connection details in each file with your actual credentials
3. Uncomment and implement the database operations as needed

## Security Considerations

When implementing these for production:

- Use prepared statements for all database queries to prevent SQL injection
- Implement proper authentication and authorization
- Validate all input thoroughly
- Consider using CSRF protection for forms
- Implement rate limiting to prevent abuse

## Example Response Format

```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {
    "id": 1234,
    "name": "Example Name",
    "other_field": "value"
  }
}
```

## Error Response Format

```json
{
  "success": false,
  "message": "Error description"
}
``` 