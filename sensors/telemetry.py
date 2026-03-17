# sensors/telemetry.py
# Simulates telemetry verification from Arduino car. Real system will be replaced by wireless or serial communicatin
import random

def telemetry_valid():
    """
    Simulate whether telemetry confirms the target.

    Returns
    ------
        True if the drone should trust the vision tracking.
    """
    return random.choice([True, True, True, False])  # 75% valid
