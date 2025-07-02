# Electron Flask Clone

This project is an Electron application that mimics the functionality of a Flask application, featuring user authentication, WebSocket communication, and video streaming capabilities.

## Project Structure

```
electron-flask-clone
├── src
│   ├── main.js          # Main entry point of the Electron application
│   ├── preload.js       # Preload script for exposing APIs to the renderer
│   ├── renderer.js      # User interface logic and interactions
│   ├── wsServer.js      # WebSocket server for communication with ROS 2 node
│   ├── videoStream.js    # UDP video streaming functionality
│   ├── users.js         # User authentication logic
│   └── views
│       ├── index.html   # Main HTML view with video feed
│       └── login.html   # Login page for user authentication
├── package.json         # npm configuration file with dependencies
└── README.md            # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd electron-flask-clone
   ```

2. **Install dependencies:**
   ```
   npm install
   ```

3. **Run the application:**
   ```
   npm start
   ```

## Usage

- Open the application and navigate to the login page to authenticate.
- After logging in, you will be redirected to the main interface where you can view the video stream and interact with the application.
- The application communicates with a ROS 2 node via WebSocket for real-time data exchange.

## Features

- User authentication with hashed passwords.
- WebSocket communication for real-time interaction.
- UDP video streaming capabilities for live video feed.

## License

This project is licensed under the MIT License.