# control/drone_controller.py

from djitellopy import Tello
import time

from control.pid import PID
from config import PID_CONFIG, OUTPUT_LIMITS, LOST_TIMEOUT, DEADBAND


class DroneController:
    def __init__(self):

        self.tello = Tello()
        self.tello.connect()
        self.tello.streamon()

        self.pid_yaw = PID(**PID_CONFIG["yaw"], output_limits=OUTPUT_LIMITS)
        self.pid_alt = PID(**PID_CONFIG["altitude"], output_limits=OUTPUT_LIMITS)
        self.pid_forward = PID(**PID_CONFIG["forward"], output_limits=OUTPUT_LIMITS)

        self.last_valid_time = time.time()

    def apply_deadband(self, error):
        return 0 if abs(error) < DEADBAND else error

    def update(self, error_x, error_y, error_z, telemetry_ok):

        error_x = self.apply_deadband(error_x)
        error_y = self.apply_deadband(error_y)
        error_z = self.apply_deadband(error_z)

        if telemetry_ok:
            self.last_valid_time = time.time()

            yaw = int(self.pid_yaw.update(error_x))
            vertical = int(self.pid_alt.update(error_y))
            forward = int(self.pid_forward.update(error_z))

            self.tello.send_rc_control(
                0,
                forward,
                vertical,
                yaw
            )

        else:
            self.recover()

    def recover(self):
        if time.time() - self.last_valid_time > LOST_TIMEOUT:
            print("Target lost. Searching...")
            self.tello.send_rc_control(0, 0, 0, 20)
        else:
            self.tello.send_rc_control(0, 0, 0, 0)


    def emergency_stop(self):
        print("EMERGENCY STOP")
        self.tello.send_rc_control(0, 0, 0, 0)

    def takeoff(self):
        self.tello.takeoff()

    def land(self):
        self.tello.land()