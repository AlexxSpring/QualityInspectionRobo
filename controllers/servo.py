import logging

try:
    from gpiozero import AngularServo
    from config.hardware import PIN_SERVO_PWM
    from gpiozero.pins.pigpio import PiGPIOFactory
    
    # Use pigpio for hardware PWM on servo to avoid jitter
    # Note: Requires pigpiod service running on Pi
    factory = PiGPIOFactory()
    servo = AngularServo(PIN_SERVO_PWM, min_angle=-90, max_angle=90, pin_factory=factory)
    HARDWARE_AVAILABLE = True
except (ImportError, Exception) as e:
    logging.warning(f"Servo hardware not available, falling back to mock. Error: {e}")
    HARDWARE_AVAILABLE = False
    servo = None

def set_servo_angle(angle: int):
    """
    Sets servo angle. Falls back to mock print if hardware is absent.
    """
    if HARDWARE_AVAILABLE and servo:
        # Clamp angle to min/max
        clamped_angle = max(-90, min(90, angle))
        servo.angle = clamped_angle
    else:
        print(f"[Hardware Mock] Setting servo angle to {angle} degrees")
        # In a real implementation we would use gpiozero or RPi.GPIO here
