import random
import logging

USE_MOCK = False
DEFAULT_IR_PIN = 17
_ir = None

try:
    from gpiozero import DigitalInputDevice
    from sys_config.hardware import PIN_IR_OUT
    IR_PIN = PIN_IR_OUT
    HARDWARE_AVAILABLE = True
except (ImportError, Exception) as e:
    logging.warning(f"IR hardware not available, falling back to mock. Error: {e}")
    HARDWARE_AVAILABLE = False
    USE_MOCK = True
    IR_PIN = DEFAULT_IR_PIN


def _get_ir():
    global _ir
    if _ir is None and HARDWARE_AVAILABLE:
        _ir = DigitalInputDevice(IR_PIN, pull_up=True)
    return _ir


def read_ir_status() -> bool:
    """
    Reads IR sensor state.
    Returns True if an object is detected, False otherwise.
    Falls back to mock data if hardware is absent.
    """
    if USE_MOCK:
        # Simulate object usually being detected
        return random.choices([True, False], weights=[0.85, 0.15])[0]

    try:
        ir = _get_ir()
        detected = (ir.value == 0)
        return detected
    except Exception as e:
        logging.warning(f"IR runtime error: {e}")
        return random.choice([True, False])
