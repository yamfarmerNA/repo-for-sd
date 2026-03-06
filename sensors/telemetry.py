# sensors/telemetry.py

import random

def telemetry_valid():
    """
    Simulates whether telemetry confirms correct target.
    """
    return random.choice([True, True, True, False])  # 75% valid