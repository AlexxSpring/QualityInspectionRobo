def set_servo_angle(angle: int):
    """
    Mock servo controller.
    """
    print(f"[Hardware Mock] Setting servo angle to {angle} degrees")
    # In a real implementation we would use gpiozero or RPi.GPIO here
