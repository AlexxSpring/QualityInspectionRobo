import logging

try:
    from gpiozero import LED
    from sys_config.hardware import PIN_LED_GREEN, PIN_LED_RED
    
    led_green = LED(PIN_LED_GREEN)
    led_red = LED(PIN_LED_RED)
    HARDWARE_AVAILABLE = True
except (ImportError, Exception) as e:
    logging.warning(f"Lighting hardware not available, falling back to mock. Error: {e}")
    HARDWARE_AVAILABLE = False
    led_green = None
    led_red = None

def set_led_state(color: str, state: str):
    """
    Sets LED state. color can be "GREEN" or "RED". state can be "ON" or "OFF".
    Falls back to mock print if hardware is absent.
    """
    if HARDWARE_AVAILABLE:
        target_led = led_green if color.upper() == "GREEN" else led_red
        if target_led:
            if state.upper() == "ON":
                target_led.on()
            elif state.upper() == "OFF":
                target_led.off()
            elif state.upper() == "TOGGLE":
                target_led.toggle()
    else:
        print(f"[Hardware Mock] Setting {color} LED to {state}")
