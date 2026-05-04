import os
os.environ["GPIOZERO_PIN_FACTORY"] = "lgpio"

import random
import logging

USE_MOCK = False
DEFAULT_IR_PIN = 17

try:
    from gpiozero import DigitalInputDevice, Device
    print("IR GPIO Factory:", Device.pin_factory)

    try:
        from sys_config.hardware import PIN_IR_OUT
        IR_PIN = PIN_IR_OUT
    except Exception as e:
        print("Using default IR pin (17):", e)
        IR_PIN = DEFAULT_IR_PIN

    _ir = None

    def _get_ir():
        global _ir
        if _ir is None:
            _ir = DigitalInputDevice(IR_PIN, pull_up=True)
        return _ir

except Exception as e:
    print("IR INIT FAILED:", e)
    logging.warning("IR hardware not available, switching to mock")
    USE_MOCK = True


def read_ir_status():
    if USE_MOCK:
        value = random.choice([True, False])
        print("[MOCK] IR:", value)
        return value

    try:
        ir = _get_ir()
        detected = (ir.value == 0)
        print("[REAL] IR:", detected)
        return detected

    except Exception as e:
        print("IR runtime error:", e)
        return random.choice([True, False])
