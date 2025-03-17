from adafruit_servokit import ServoKit
import socket

"""
Servo Control Server

This script sets up a TCP server that listens for incoming connections, receives finger angle 
commands from a client, and moves the corresponding servos using the Adafruit ServoKit library.
Each finger is mapped to a specific servo, and the server applies the received angles to control 
the servos accordingly. The angle is inverted to ensure natural finger movement.

Author: Paola Gabriela Lomeli Barcena
Date: 30 Jan 2025

Dependencies:
- adafruit_servokit
- socket

Usage:
- Run this script on the Raspberry Pi connected to the PCA9685 servo controller.
- Ensure the client is running and sending the expected finger angle data in the format:
  "finger_id,angle;finger_id,angle;...".
- The server will process the data and move the servos to the specified angles.
"""

# Initialize the PCA9685 controller
kit = ServoKit(channels=8)

# Server configuration
server_ip = '0.0.0.0'  # Listen on all interfaces
server_port = 65432

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
sock.bind((server_ip, server_port))

# Listen for incoming connections
sock.listen(1)

print('Waiting for a connection...')

# Accept a connection
connection, client_address = sock.accept()

finger_to_servo_map = {
    0: 0,  # Thumb  -> Servo 0
    1: 1,  # Index  -> Servo 1
    2: 2,  # Middle -> Servo 2
    3: 3,  # Ring   -> Servo 3
    4: 4   # Pinky  -> Servo 4
}

try:
    print('Conectado a:', client_address)

    while True:
        # Receive data from the client
        data = connection.recv(1024)
        if not data:
            break

        try:
            # Decode and process the received data
            # Expected format: "finger_id,angle;finger_id,angle;..."
            commands = data.decode('utf-8').strip().split(';')
            print(f"Received commands: {commands}")

            # Receive data and move the servos accordingly
            for command in commands:
                try:
                    finger_id, angle = map(int, command.split(','))
                    if 0 <= finger_id < 5 and 0 <= angle <= 180:
                        # Map the finger_id to the corresponding servo channel
                        servo_channel = finger_to_servo_map.get(finger_id)
                        if servo_channel is not None:
                            # Apply the angle (invert angle for natural behavior)
                            inverted_angle = 180 - angle
                            kit.servo[servo_channel].angle = inverted_angle
                            print(f"Moved finger {finger_id} to angle {inverted_angle}")
                        else:
                            print(f"Finger {finger_id} not mapped to a servo")
                    else:
                        print(f"Invalid finger_id or angle: {command}")
                except ValueError as e:
                    print(f"Error parsing command '{command}': {e}")

        except Exception as e:
            print(f"Error processing data: {e}")

finally:
    connection.close()
    sock.close()
