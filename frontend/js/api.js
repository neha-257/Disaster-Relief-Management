// API URL configuration
const API_BASE_URL = 'http://localhost:5000/api';

// Generic fetch function for API calls
async function fetchAPI(endpoint, method = 'GET', data = null) {
    const url = `${API_BASE_URL}/${endpoint}`;
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json'
        }
    };

    if (data && (method === 'POST' || method === 'PUT')) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(url, options);
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.message || 'An error occurred');
        }
        
        return result;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Relief Camp API functions
const reliefCampAPI = {
    // Get all relief camps
    getAll: () => fetchAPI('relief_camps'),
    
    // Get a single relief camp by ID
    getById: (id) => fetchAPI(`relief_camps/${id}`),
    
    // Create a new relief camp
    create: (campData) => fetchAPI('relief_camps', 'POST', campData),
    
    // Update an existing relief camp
    update: (id, campData) => fetchAPI(`relief_camps/${id}`, 'PUT', campData),
    
    // Delete a relief camp
    delete: (id) => fetchAPI(`relief_camps/${id}`, 'DELETE')
};

// Victim Management API functions
const victimAPI = {
    // Get all victims
    getAll: () => fetchAPI('victims'),
    
    // Get a single victim by ID
    getById: (id) => fetchAPI(`victims/${id}`),
    
    // Create a new victim
    create: (victimData) => fetchAPI('victims', 'POST', victimData),
    
    // Update an existing victim
    update: (id, victimData) => fetchAPI(`victims/${id}`, 'PUT', victimData),
    
    // Delete a victim
    delete: (id) => fetchAPI(`victims/${id}`, 'DELETE')
};

// Missing Person API functions
const missingPersonAPI = {
    // Get all missing person reports
    getAll: () => fetchAPI('missing_persons'),
    
    // Get a single missing person report by ID
    getById: (id) => fetchAPI(`missing_persons/${id}`),
    
    // Create a new missing person report
    create: (reportData) => fetchAPI('missing_persons', 'POST', reportData),
    
    // Update an existing missing person report
    update: (id, reportData) => fetchAPI(`missing_persons/${id}`, 'PUT', reportData),
    
    // Delete a missing person report
    delete: (id) => fetchAPI(`missing_persons/${id}`, 'DELETE')
};

// Inventory API functions
const inventoryAPI = {
    // Get all inventory items
    getAll: () => fetchAPI('inventory'),
    
    // Get a single inventory item by ID
    getById: (id) => fetchAPI(`inventory/${id}`),
    
    // Create a new inventory item
    create: (itemData) => fetchAPI('inventory', 'POST', itemData),
    
    // Update an existing inventory item
    update: (id, itemData) => fetchAPI(`inventory/${id}`, 'PUT', itemData),
    
    // Delete an inventory item
    delete: (id) => fetchAPI(`inventory/${id}`, 'DELETE')
};

// Volunteer API functions
const volunteerAPI = {
    // Get all volunteers
    getAll: () => fetchAPI('volunteers'),
    
    // Get a single volunteer by ID
    getById: (id) => fetchAPI(`volunteers/${id}`),
    
    // Create a new volunteer
    create: (volunteerData) => fetchAPI('volunteers', 'POST', volunteerData),
    
    // Update an existing volunteer
    update: (id, volunteerData) => fetchAPI(`volunteers/${id}`, 'PUT', volunteerData),
    
    // Delete a volunteer
    delete: (id) => fetchAPI(`volunteers/${id}`, 'DELETE')
};

// Contact form API function
const contactAPI = {
    // Submit contact form
    submit: (formData) => fetchAPI('contact', 'POST', formData)
};

// DOM Helper functions
function showAlert(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Find a suitable container to show the alert
    const container = document.querySelector('.container') || document.body;
    container.prepend(alertDiv);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.parentNode.removeChild(alertDiv);
        }
    }, 5000);
}

// Form data to JSON helper
function formToJSON(form) {
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        // Convert empty strings to null
        data[key] = value === '' ? null : value;
    }
    
    return data;
} 