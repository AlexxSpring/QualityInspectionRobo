import random
import time
import logging

try:
    from hx711 import HX711
    from sys_config.hardware import PIN_HX711_DT, PIN_HX711_SCK, LOADCELL_CALIBRATION_FACTOR
    
    # Initialize HX711
    hx = HX711(dout_pin=PIN_HX711_DT, pd_sck_pin=PIN_HX711_SCK)
    hx.set_scale_ratio(LOADCELL_CALIBRATION_FACTOR)
    # Give it time to settle
    time.sleep(0.5)
    hx.reset()
    hx.tare()
    HARDWARE_AVAILABLE = True
except (ImportError, Exception) as e:
    logging.warning(f"Load cell hardware not available, falling back to mock. Error: {e}")
    HARDWARE_AVAILABLE = False
    hx = None

def read_weight() -> float:
    """
    Reads load cell value.
    Returns weight in kg. Falls back to mock data.
    """
    if HARDWARE_AVAILABLE and hx:
        # Assuming calibration factor is set such that get_weight_mean returns kg
        try:
            val = hx.get_weight_mean(5)
            return round(val, 2)
        except Exception as e:
            logging.error(f"Error reading HX711: {e}")
            return 0.0
    else:
        # Simulate a value fluctuating around 2.5kg
        base_weight = 2.5
        noise = random.uniform(-0.1, 0.1)
        return round(base_weight + noise, 2)
