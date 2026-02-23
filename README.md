# Disaster Relief Management System

A comprehensive disaster relief management system that includes modules for victim management, missing person reports, relief camps, inventory management, volunteer coordination, and donation tracking.

## System Architecture

- **Frontend**: HTML, CSS, JavaScript with Bootstrap framework
- **Backend**: Python Flask API
- **Database**: MySQL

## Features

- **Victim Management**: Register and track victims
- **Missing Person Reports**: Submit and search for missing persons
- **Relief Camps**: Manage relief camps and shelters
- **Inventory Management**: Track relief supplies and materials
- **Volunteer Coordination**: Register and assign volunteers
- **Donation Tracking**: Record and manage donations

## Prerequisites

- Python 3.6+
- Node.js (to run the start script)
- MySQL database

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone https://github.com/yourusername/DisasterReliefManagement.git
   cd DisasterReliefManagement
   ```

2. **Set up the MySQL database**:
   - Create a MySQL database
   - Import the database schema from `backend/db.sql`
   
3. **Configure environment variables**:
   - Update the `.env` file in the backend directory with your MySQL connection details:
   ```
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=yourpassword
   DB_NAME=disaster_relief
   ```

4. **Install backend dependencies**:
   ```
   pip install -r backend/requirements.txt
   ```

5. **Start the application**:
   
   Using Node.js:
   ```
   node start.js
   ```
   
   Or start Flask directly:
   ```
   cd backend
   python app.py
   ```

6. **Access the application**:
   - Backend API: `http://localhost:5000`
   - Frontend: Open the HTML files in the `frontend` directory directly in your browser

## API Documentation

The backend provides the following API endpoints:

- **Relief Camps**: `/api/relief_camps`
- **Victims**: `/api/victims`
- **Missing Persons**: `/api/missing_persons`
- **Inventory**: `/api/inventory`
- **Volunteers**: `/api/volunteers`
- **Contact Form**: `/api/contact`

Each endpoint supports standard CRUD operations:
- `GET /api/[resource]` - Get all resources
- `GET /api/[resource]/:id` - Get a specific resource
- `POST /api/[resource]` - Create a new resource
- `PUT /api/[resource]/:id` - Update a resource
- `DELETE /api/[resource]/:id` - Delete a resource

## Project Structure

```
DisasterReliefManagement/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── config.py           # Configuration settings
│   ├── .env                # Environment variables
│   ├── requirements.txt    # Python dependencies
│   └── db.sql              # Database schema
├── frontend/
│   ├── assets/             # CSS, JS, and image assets
│   ├── js/                 # JavaScript files
│   │   └── api.js          # API communication module
│   ├── css/                # CSS stylesheets
│   ├── index.html          # Homepage
│   ├── relief-camps.html   # Relief camps page
│   ├── victim-management.html # Victim management page
│   ├── missing-persons.html # Missing persons page
│   ├── inventory.html      # Inventory management page
│   ├── volunteers.html     # Volunteer coordination page
│   └── donations.html      # Donation tracking page
├── start.js                # Node.js script to start the application
└── README.md               # This file
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
