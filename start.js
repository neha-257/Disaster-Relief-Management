const { spawn } = require('child_process');
const path = require('path');
const os = require('os');

// Detect platform
const isWindows = os.platform() === 'win32';

// Command to run based on platform
const command = isWindows ? 'python' : 'python3';

// Path to the backend app
const backendPath = path.join(__dirname, 'backend', 'app.py');

console.log('Starting Disaster Relief Management System...');
console.log('Starting Flask backend server...');

// Spawn the Python Flask process
const flaskProcess = spawn(command, [backendPath], {
  stdio: 'inherit'
});

// Handle process exit
flaskProcess.on('close', (code) => {
  if (code !== 0) {
    console.error(`Flask process exited with code ${code}`);
  }
  console.log('Flask server stopped');
});

// Handle SIGINT (Ctrl+C)
process.on('SIGINT', () => {
  console.log('Stopping Flask server...');
  flaskProcess.kill('SIGINT');
  process.exit(0);
});

console.log('Backend server started at http://localhost:5000');
console.log('---------------------------------------------');
console.log('To access the application:');
console.log('1. Open http://localhost:5000 in your browser for the API');
console.log('2. Open the frontend/index.html file in your browser for the frontend');
console.log('3. Press Ctrl+C to stop the server');
console.log('---------------------------------------------'); 