# config.py

PID_CONFIG = {
    "yaw": {"Kp": 0.4, "Ki": 0.0, "Kd": 0.2},
    "altitude": {"Kp": 0.5, "Ki": 0.0, "Kd": 0.25},
    "forward": {"Kp": 0.6, "Ki": 0.0, "Kd": 0.3},
}

OUTPUT_LIMITS = (-100, 100)

LOST_TIMEOUT = 2.0
DEADBAND = 0.05