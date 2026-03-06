# main.py

from control.drone_controller import DroneController
from sensors.vision import get_vision_error
from sensors.telemetry import telemetry_valid
import time

def main():

    controller = DroneController()
    controller.takeoff()

    try:
        while True:
            error_x, error_y, error_z = get_vision_error()
            valid = telemetry_valid()

            controller.update(error_x, error_y, error_z, valid)

            time.sleep(0.05)  # 20 Hz loop

    except KeyboardInterrupt:
        print("Landing...")
        controller.land()


if __name__ == "__main__":
    main()
