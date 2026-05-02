def set_light_state(state: str, brightness: int = 100):
    """
    Mock lighting controller.
    """
    print(f"[Hardware Mock] Setting light to {state} with {brightness}% brightness")
    # In a real implementation we would use GPIO PWM here
