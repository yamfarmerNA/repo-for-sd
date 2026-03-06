import random

def get_vision_error():
    """
    Returns normalized errors:
    error_x: -1 to 1
    error_y: -1 to 1
    error_z: distance error
    """

    # Mock values for testing
    error_x = random.uniform(-0.2, 0.2)
    error_y = random.uniform(-0.2, 0.2)
    error_z = random.uniform(-0.3, 0.3)

    return error_x, error_y, error_z