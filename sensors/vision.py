# Provides target tracking errors based on camera input.

# Currently generates simulated values for testing, later will be replaced with object tracking.
import random

def get_vision_error():
    """
    Simulates vision tracking errors
    
    Returns normalized errors:
    error_x: Horizontal offset from center (-1 to 1)
    error_y: Vertical offset from center (-1 to 1)
    error_z: Distance error based on target size
    """

    # Mock values for testing
    error_x = random.uniform(-0.2, 0.2)
    error_y = random.uniform(-0.2, 0.2)
    error_z = random.uniform(-0.3, 0.3)

    return error_x, error_y, error_z
