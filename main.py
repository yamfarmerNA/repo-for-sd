# main.py
# This script initializes the controller and continuously updates the drone based on sensor inputs.

from control.drone_controller import DroneController
from sensors.vision import get_vision_error
from sensors.telemetry import telemetry_valid
import time

def main():
    '''
    Main control loop 
    '''
    
    controller = DroneController()

    # start flight
    controller.takeoff()

    try:
        while True:
             # Get tracking errors from vision system
            error_x, error_y, error_z = get_vision_error()

            # Verify target using telemetry
            valid = telemetry_valid()

            # Update drone controller
            controller.update(error_x, error_y, error_z, valid)

            # Maintain ~20 Hz control loop
            time.sleep(0.05)  # 20 Hz loop

    except KeyboardInterrupt:
        print("Keyboard interrupt detected.")

    finally:

        # -------------------------------------------------
        # Guaranteed safe shutdown
        # -------------------------------------------------
        print("Shutting down safely...")

        controller.emergency_stop()
        time.sleep(0.5)

        controller.land()

        print("Drone landed.")


if __name__ == "__main__":
    main()
