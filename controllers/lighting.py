import logging

try:
    from gpiozero import PWMOutputDevice
    from sys_config.hardware import PIN_LIGHT_PWM
    
    light = PWMOutputDevice(PIN_LIGHT_PWM)
    HARDWARE_AVAILABLE = True
except (ImportError, Exception) as e:
    logging.warning(f"Lighting hardware not available, falling back to mock. Error: {e}")
    HARDWARE_AVAILABLE = False
    light = None

def set_light_state(state: str, brightness: int = 100):
    """
    Sets light state and brightness. Falls back to mock print if hardware is absent.
    """
    if HARDWARE_AVAILABLE and light:
        if state.upper() == "ON":
            light.value = brightness / 100.0
        elif state.upper() == "OFF":
            light.value = 0.0
        elif state.upper() == "TOGGLE":
            light.toggle()
    else:
        print(f"[Hardware Mock] Setting light to {state} with {brightness}% brightness")
        # In a real implementation we would use GPIO PWM here
