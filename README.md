# Interactive Menu Selection Using Hand Gestures

This project presents a contactless menu navigation system using hand gesture recognition. Users can interact with a digital menu by showing a specific number of fingers to select an item. The system uses a webcam, real-time hand tracking, and gesture detection to operate without physical contact.

## Project Description

The application uses Python, MediaPipe, and OpenCV to detect hand gestures from webcam input. A Flask server processes the gestures and updates the menu accordingly. The frontend communicates with the backend using Socket.IO, allowing real-time updates in the browser.

### Key Features

- Detects the number of fingers held up.
- Allows users to navigate a menu and make selections without touching the screen.
- Each gesture must be held for 3 seconds to confirm a selection.
- Displays total cost and selected items in real time.
- Menu includes categories like coffee, tea, snacks, and checkout.

## Technologies Used

- Python
- Flask and Flask-SocketIO
- OpenCV
- MediaPipe
- HTML, CSS, JavaScript

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/gesture-menu.git
   cd gesture-menu
