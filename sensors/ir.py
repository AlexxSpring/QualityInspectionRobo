import random
import logging

try:
    from gpiozero import DigitalInputDevice
    from config.hardware import PIN_IR_OUT
    
    # Initialize the sensor. IR obstacle sensors are often active LOW.
    ir_sensor = DigitalInputDevice(PIN_IR_OUT, pull_up=True)
    HARDWARE_AVAILABLE = True
except (ImportError, Exception) as e:
    logging.warning(f"IR hardware not available, falling back to mock. Error: {e}")
    HARDWARE_AVAILABLE = False
    ir_sensor = None

def read_ir_status() -> bool:
    """
    Reads IR sensor status.
    Returns True if object is detected, False otherwise. Falls back to mock data.
    """
    if HARDWARE_AVAILABLE and ir_sensor:
        # Assuming active LOW (0 = object detected)
        return not ir_sensor.value
    else:
        # Simulate an object being detected 80% of the time
        return random.random() < 0.8
