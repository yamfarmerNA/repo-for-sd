# control/drone_controller.py
# Handles communication with drone and applies PID control outputs to generate flight commands.

from djitellopy import Tello
import time

from control.pid import PID
from config import PID_CONFIG, OUTPUT_LIMITS, LOST_TIMEOUT, DEADBAND


class DroneController:
    def __init__(self):
        ''' 
        Initialize drone connection and control components.
        '''
        # connect to drone
        self.tello = Tello()
        self.tello.connect()

        # enable camera on
        self.tello.streamon()

         # Create separate PID controllers for each axis of motion
        self.pid_yaw = PID(**PID_CONFIG["yaw"], output_limits=OUTPUT_LIMITS)
        self.pid_alt = PID(**PID_CONFIG["altitude"], output_limits=OUTPUT_LIMITS)
        self.pid_forward = PID(**PID_CONFIG["forward"], output_limits=OUTPUT_LIMITS)

        # Track when telemetry was last valid
        self.last_valid_time = time.time()

    
    def apply_deadband(self, error):
        '''
        Ignore small errors that fall within the deadband threshold.
        '''
        return 0 if abs(error) < DEADBAND else error

    def update(self, error_x, error_y, error_z, telemetry_ok):
        '''
        Main control update function called every loop iteration.
        '''

        # apply deadband filtering
        error_x = self.apply_deadband(error_x)
        error_y = self.apply_deadband(error_y)
        error_z = self.apply_deadband(error_z)

        if telemetry_ok:
            # Record the last time the target was confirmed
            self.last_valid_time = time.time()

            # Compute PID corrections for each axis
            yaw = int(self.pid_yaw.update(error_x))
            vertical = int(self.pid_alt.update(error_y))
            forward = int(self.pid_forward.update(error_z))

            # Send velocity command to drone
            self.tello.send_rc_control(
                0,
                forward,
                vertical,
                yaw
            )

        else:
            self.recover()

    def recover(self):
        '''
        Recovery behavior when the target is lost.
        '''
        if time.time() - self.last_valid_time > LOST_TIMEOUT:
            print("Target lost. Searching...")
            # Slow rotation to scan environment
            self.tello.send_rc_control(0, 0, 0, 20)

            # Hover temporarily while waiting for signal
        else:
            self.tello.send_rc_control(0, 0, 0, 0)


    def emergency_stop(self):
        print("EMERGENCY STOP")
        self.tello.send_rc_control(0, 0, 0, 0)

    def takeoff(self):
        self.tello.takeoff()

    def land(self):
        self.tello.land()
