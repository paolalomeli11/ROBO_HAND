import subprocess
import time
import sys

def run_servo_control_server():
    subprocess.Popen([sys.executable, 'servo_control.py'])

def run_hand_tracking():
    subprocess.Popen([sys.executable, 'hand_tracking.py'])

if __name__ == "__main__":
    run_servo_control_server()
    time.sleep(5)
    run_hand_tracking()
    
    input("Press Enter to exit...\n")
