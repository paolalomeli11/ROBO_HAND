import mediapipe as mp
import socket
import math
import cv2

"""
Hand Tracking and Finger Angle Detection

This script captures hand movements using OpenCV and MediaPipe, calculates finger angles,
and sends the data to a Raspberry Pi server over a socket connection. The thumb is processed
differently, considering its unique range of motion relative to the palm.

Author: Paola Gabriela Lomeli Barcena
Date: 30 Jan 2025

Dependencies:
- OpenCV
- MediaPipe
- socket

Usage:
- Run this script on the raspberry pi or on a machine with a webcam.
- Ensure the Raspberry Pi server is running and listening on the specified port.
- The program will send detected finger angles to the Raspberry Pi for further processing.

"""

# Socket configuration
server_ip = '127.0.0.1'          #Loopback IP if running servo control on raspberry pi
server_port = 65432

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((server_ip, server_port))

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

scaling_factor = 1000
movement_threshold = 5

last_angles = {finger_id: None for finger_id in range(0, 5)}

with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                messages = []
                
                for finger_id in range(1, 5):  # 1 = Index, 2 = Middle, 3 = Ring, 4 = Pinky
                    try:
                        joint1 = hand_landmarks.landmark[finger_id * 4 + 1]
                        joint2 = hand_landmarks.landmark[finger_id * 4 + 3]

                        # Calculate the distance between joints
                        distance = ((joint1.x - joint2.x) ** 2 + (joint1.y - joint2.y) ** 2) ** 0.5

                        # Map the distance to an angle between 0 and 180 degrees
                        angle = int(min(distance * scaling_factor, 180))

                        # Check if the angle change is significant
                        if last_angles[finger_id] is None or abs(angle - last_angles[finger_id]) >= movement_threshold:
                            last_angles[finger_id] = angle
                            messages.append(f"{finger_id},{angle}")

                    except IndexError:
                        print(f"Error: Could not process finger with ID {finger_id}")

                # Special handling for thumb (finger_id = 0)
                try:
                    wrist = hand_landmarks.landmark[0]
                    thumb_tip = hand_landmarks.landmark[4]
                    thumb_mcp = hand_landmarks.landmark[2]

                    # Calculate the angle of the thumb relative to the wrist
                    vec_thumb = (thumb_tip.x - thumb_mcp.x, thumb_tip.y - thumb_mcp.y)
                    vec_wrist = (wrist.x - thumb_mcp.x, wrist.y - thumb_mcp.y)
                    dot_product = vec_thumb[0] * vec_wrist[0] + vec_thumb[1] * vec_wrist[1]
                    mag_thumb = math.sqrt(vec_thumb[0]**2 + vec_thumb[1]**2)
                    mag_wrist = math.sqrt(vec_wrist[0]**2 + vec_wrist[1]**2)
                    angle = math.degrees(math.acos(dot_product / (mag_thumb * mag_wrist)))

                    # Check if the angle change is significant
                    if last_angles[0] is None or abs(angle - last_angles[0]) >= movement_threshold:
                        last_angles[0] = angle
                        messages.append(f"0,{int(angle)}")
                except IndexError:
                    print("Error: Could not process thumb")

                # Send all messages
                if messages:
                    sock.sendall(';'.join(messages).encode('utf-8'))

        cv2.imshow('Hand Tracking', image)

        if cv2.waitKey(5) & 0xFF == 27:  # Exit when 'Esc' is pressed
            break

sock.close()
cap.release()
cv2.destroyAllWindows()
