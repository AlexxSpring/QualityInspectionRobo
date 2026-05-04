import os
os.environ["GPIOZERO_PIN_FACTORY"] = "lgpio"
import random
import logging

try:
    from gpiozero import DistanceSensor
    from sys_config.hardware import PIN_ULTRASONIC_ECHO, PIN_ULTRASONIC_TRIGGER
    
    # Initialize the sensor using configuration
    sensor = DistanceSensor(echo=PIN_ULTRASONIC_ECHO, trigger=PIN_ULTRASONIC_TRIGGER)
    HARDWARE_AVAILABLE = True
    logging.info(f"Ultrasonic sensor initialized successfully on pins {PIN_ULTRASONIC_ECHO}/{PIN_ULTRASONIC_TRIGGER}")
except (ImportError, Exception) as e:
    logging.error(f"Ultrasonic hardware not available, falling back to mock. Error: {e}")
    HARDWARE_AVAILABLE = False
    sensor = None

def read_distance() -> float:
    """
    Reads distance from ultrasonic sensor.
    Returns distance in cm. Falls back to mock data if hardware is absent.
    """
    if HARDWARE_AVAILABLE and sensor:
        # gpiozero DistanceSensor returns distance in meters, convert to cm
        return round(sensor.distance * 100, 2)
    else:
        # Simulate an object being around 15cm away
        base_dist = 15.0
        noise = random.uniform(-0.5, 0.5)
        return round(base_dist + noise, 2)
