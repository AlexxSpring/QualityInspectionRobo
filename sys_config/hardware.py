"""
Centralized Hardware Configuration
Fill in the correct BCM pin numbers once the physical wiring is finalized.
"""

# --- Ultrasonic Sensor ---
PIN_ULTRASONIC_TRIGGER = 23
PIN_ULTRASONIC_ECHO = 24

# --- IR Sensor ---
PIN_IR_OUT = 25

# --- Load Cell (HX711) ---
PIN_HX711_DT = 5
PIN_HX711_SCK = 6
LOADCELL_CALIBRATION_FACTOR = 1.0 # Update this after calibrating with a known weight

# --- Servo Motor ---
PIN_SERVO_PWM = 12

# --- Lighting / LED ---
PIN_LED_GREEN = 13
PIN_LED_RED = 19
