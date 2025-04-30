import time
from flask import Flask, render_template
from flask_socketio import SocketIO
import cv2
import base64
import mediapipe as mp
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for the Flask app
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow all origins

# Initialize MediaPipe Hand module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Global variables for menu logic
menu = 'Home'
check = 0
previous_selected_option = None
menu_change_start_time = None
def count_raised_fingers(hand_landmarks):
    raised_fingers = 0
    for finger_tip, finger_base in zip(
        [mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.INDEX_FINGER_TIP,
         mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_TIP,
         mp_hands.HandLandmark.PINKY_TIP],
        [mp_hands.HandLandmark.THUMB_IP, mp_hands.HandLandmark.INDEX_FINGER_MCP,
         mp_hands.HandLandmark.MIDDLE_FINGER_MCP, mp_hands.HandLandmark.RING_FINGER_MCP,
         mp_hands.HandLandmark.PINKY_MCP]
    ):
        if finger_tip == mp_hands.HandLandmark.THUMB_TIP:
            if hand_landmarks.landmark[finger_tip].y > hand_landmarks.landmark[finger_base].y:
                raised_fingers += 1
        else:
            if hand_landmarks.landmark[finger_tip].y < hand_landmarks.landmark[finger_base].y:
                raised_fingers += 1
    return raised_fingers

@socketio.on('send_frame')
def handle_frame(data):
    global menu, check,previous_selected_option,menu_change_start_time
    # Decode the received frame
    frame_data = base64.b64decode(data)
    np_frame = np.frombuffer(frame_data, dtype=np.uint8)
    frame = cv2.imdecode(np_frame, cv2.IMREAD_COLOR)

    # Process the frame with MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Count the number of raised fingers
            num_raised_fingers = count_raised_fingers(hand_landmarks)
            # cv2.putText(frame, f"Total: {check} L.E", (400, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            # Loop through fingers to check if they are raised
            num_raised_fingers = count_raised_fingers(hand_landmarks)
            
            # Draw landmarks on the frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            selected_option = num_raised_fingers
            if menu =='Home':
                # Display the menu options
                cv2.putText(frame, "1. Coffee", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(frame, "2. Tea", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(frame, "3. Snacks", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(frame, "4. Checkout ", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(frame, "5. Exit", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                if selected_option == previous_selected_option:
                        if selected_option is not None:
                            if menu_change_start_time is None:
                                menu_change_start_time = time.time()
                            else:
                                elapsed_time = time.time() - menu_change_start_time
                                if elapsed_time >= 3:
                                    if selected_option == 1:
                                        menu = 'Coffee'
                                    elif selected_option == 2:
                                        menu = 'Tea'
                                    elif selected_option == 3:
                                        menu = 'Snacks'
                                    elif selected_option == 4:
                                        print(f'Your Total is {check} L.E' )
                                        socketio.emit('update_message', f'Your Total is {check} L.E')
                                        break                                         
                                    elif selected_option == 5:
                                        print(f'Your Total is {check} L.E' )
                                        # cap.release()
                                        # cv2.destroyAllWindows()
                                        break
                                    # Release video capture and close windows
                                    menu_change_start_time = None
                                    num_raised_fingers = 0
                        else:
                            menu_change_start_time = None
                else:
                        menu_change_start_time = None
            elif menu == 'Coffee':
                cv2.putText(frame, "1. Cappuccino 15 L.E", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(frame, "2. Espresso 12 L.E", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(frame, "3. Latte 14 L.E", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(frame, "4. Checkout ", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(frame, "5. Back ", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                if selected_option == previous_selected_option:
                        if selected_option is not None:
                            if menu_change_start_time is None:
                                menu_change_start_time = time.time()
                            else:
                                elapsed_time = time.time() - menu_change_start_time
                                if elapsed_time >= 3:
                                    if selected_option == 1:
                                        check += 15
                                        socketio.emit('update_message', f'Cappuccino added, your total is {check} L.E')
                                    elif selected_option == 2:
                                        check +=12
                                        socketio.emit('update_message', f'Espresso added, your total is {check} L.E')
                                    elif selected_option == 3:
                                        check +=14
                                        socketio.emit('update_message', f'latte added, your total is {check} L.E')
                                    elif selected_option == 4:
                                        socketio.emit(f'Your Total is {check} L.E' )
                                        break                                        
                                    elif selected_option == 5:
                                        menu = 'Home'
                                    menu_change_start_time = None
                                    num_raised_fingers = 0
                        else:
                            menu_change_start_time = None
                else:
                        menu_change_start_time = None
            elif menu == 'Tea':
                cv2.putText(frame, "1. green Tea 8 L.E", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(frame, "2. Earl Grey Tea 10 L.E", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(frame, "3. Herbal Tea 15 L.E", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(frame, "4. Checkout ", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(frame, "5. Back ", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                if selected_option == previous_selected_option:
                        if selected_option is not None:
                            if menu_change_start_time is None:
                                menu_change_start_time = time.time()
                            else:
                                elapsed_time = time.time() - menu_change_start_time
                                if elapsed_time >= 3:
                                    if selected_option == 1:
                                        check += 8
                                        socketio.emit('update_message', f'Green tea added, your total is {check} L.E')
                                    elif selected_option == 2:
                                        check +=10
                                        socketio.emit('update_message', f'Earl Grey tea added, your total is {check} L.E')
                                    elif selected_option == 3:
                                        check +=15
                                        socketio.emit('update_message', f'Herbal tea added, your total is {check} L.E')
                                    elif selected_option == 4:
                                        socketio.emit(f'Your Total is {check} L.E' )
                                        break
                                    elif selected_option == 5:
                                        menu = 'Home'
                                    menu_change_start_time = None
                                    num_raised_fingers = 0
                        else:
                            menu_change_start_time = None
                else:
                        menu_change_start_time = None
            elif menu == 'Snacks':
                cv2.putText(frame, "1. Chips 15 L.E", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(frame, "2. Cookies 10 L.E", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(frame, "3. PopCorn 15 L.E", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(frame, "4. Checkout ", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(frame, "5. Back ", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

                if selected_option == previous_selected_option:
                        if selected_option is not None:
                            if menu_change_start_time is None:
                                menu_change_start_time = time.time()
                            else:
                                elapsed_time = time.time() - menu_change_start_time
                                if elapsed_time >= 3:
                                    if selected_option == 1:
                                        check += 15
                                        socketio.emit('update_message', f'Chips added, your total is {check} L.E')
                                    elif selected_option == 2:
                                        check +=10
                                        socketio.emit('update_message', f'Cookies added, your total is {check} L.E')
                                    elif selected_option == 3:
                                        check +=15
                                        socketio.emit('update_message', f'Popcorn added, your total is {check} L.E')
                                    elif selected_option == 4:
                                        socketio.emit(f'Your Total is {check} L.E' )
                                        break
                                    elif selected_option == 5:
                                        menu = 'Home'
                                    menu_change_start_time = None
                                    num_raised_fingers = 0
                        else:
                            menu_change_start_time = None
                else:
                        menu_change_start_time = None
            selected_option = num_raised_fingers


            previous_selected_option = selected_option

            # Highlight the selected option
            if selected_option is not None:
                y_position = selected_option * 50  # Adjust the y-position based on option number
                cv2.rectangle(frame, (30, y_position - 30), (400, y_position + 20), (0, 255, 0), 2)

    # Encode the processed frame
    _, buffer = cv2.imencode('.jpg', frame)
    frame_base64 = base64.b64encode(buffer).decode('utf-8')
    time.sleep(0.1)
    # Send the processed frame back to the frontend
    socketio.emit('receive_frame', frame_base64)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)