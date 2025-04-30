Interactive Menu Selection Using Hand Gestures
This project presents a contactless menu navigation system using hand gesture recognition. Users can interact with a digital menu by showing a specific number of fingers to select an item. The system uses a webcam, real-time hand tracking, and gesture detection to operate without physical contact.

Project Description
The application uses Python, MediaPipe, and OpenCV to detect hand gestures from webcam input. A Flask server processes the gestures and updates the menu accordingly. The frontend communicates with the backend using Socket.IO, allowing real-time updates in the browser.

Key Features
Detects the number of fingers held up.

Allows users to navigate a menu and make selections without touching the screen.

Each gesture must be held for 3 seconds to confirm a selection.

Displays total cost and selected items in real time.

Menu includes categories like coffee, tea, snacks, and checkout.

Technologies Used
Python

Flask and Flask-SocketIO

OpenCV

MediaPipe

HTML, CSS, JavaScript (for frontend interaction)

Installation
Clone the repository:

bash
Copy
Edit
git clone https://github.com/yourusername/gesture-menu.git
cd gesture-menu
Install the required Python packages:

bash
Copy
Edit
pip install flask flask-socketio flask-cors opencv-python mediapipe numpy
Run the application:

bash
Copy
Edit
python app.py
Open the browser to the address provided (usually http://localhost:5000).

How to Use
Use your webcam to display your hand.

Show 1 to 5 fingers to select an option.

Hold the gesture for 3 seconds to confirm your choice.

Navigate through menus and select items.

Select "Checkout" to view your order summary.

Use 5 fingers to go back or exit a menu.

Folder Structure
php
Copy
Edit
├── app.py             # Backend server
├── templates/
│   └── index.html     # Frontend HTML page
├── static/
│   └── script.js      # Frontend JavaScript for webcam and sockets
Future Improvements
Improve gesture accuracy and stability.

Add sound or visual confirmation for selections.

Support additional languages.

Deploy on cloud for remote access.

License
This project is licensed under the MIT License.

