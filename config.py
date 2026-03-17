# config.py
#This file stores all configurable parameters for the drone control system.

# PID controller gains for each motion axis
# -------------------------------------------------------------------
# Each axis of motion has its own PID controller.



PID_CONFIG = {
    # Controls horizontal rotation of the drone
    # Used to keep the target centered left/right in the camera
    "yaw": {"Kp": 0.4, # proportional gain
            "Ki": 0.0, # integral gain
            "Kd": 0.2 # derivative gain
           }, 

    # Controls vertical movement
    # Keeps the target centered vertically in the camera frame
    "altitude": {"Kp": 0.5, "Ki": 0.0, "Kd": 0.25},

    # Controls forward/backward movement
    # Keeps the drone at the correct distance from the target
    "forward": {"Kp": 0.6, "Ki": 0.0, "Kd": 0.3},
}

# Output limits for PID controllers
# The Tello accepts control values between -100 and 100.
# Edit parameter to restrict the range to avoid aggressive movements.
OUTPUT_LIMITS = (-100, 100)

# Lost target timeout
# If telemetry has not confirmed the target for this many seconds, the drone assumes it lost the target and enters search mode
LOST_TIMEOUT = 2.0


# Deadband threshold
# Small errors below this value are ignored to prevent constant micro-adjustments due to sensor noise.
DEADBAND = 0.05
