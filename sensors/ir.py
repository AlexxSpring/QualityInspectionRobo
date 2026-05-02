import random

def read_ir_status() -> bool:
    """
    Mock IR sensor reading.
    Returns True if object is detected, False otherwise.
    """
    # Simulate an object being detected 80% of the time
    return random.random() < 0.8
