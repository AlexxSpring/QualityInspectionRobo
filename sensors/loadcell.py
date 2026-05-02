import random
import time

def read_weight() -> float:
    """
    Mock load cell reading.
    Returns weight in kg.
    """
    # Simulate a value fluctuating around 2.5kg
    base_weight = 2.5
    noise = random.uniform(-0.1, 0.1)
    return round(base_weight + noise, 2)
