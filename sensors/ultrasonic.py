import random

def read_distance() -> float:
    """
    Mock ultrasonic sensor reading.
    Returns distance in cm.
    """
    # Simulate an object being around 15cm away
    base_dist = 15.0
    noise = random.uniform(-0.5, 0.5)
    return round(base_dist + noise, 2)
