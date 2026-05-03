from sensors.ultrasonic import read_distance
from sensors.ir import read_ir_status
from sys_config.thresholds import DISTANCE_MAX, IR_EXPECTED_DETECTED
from controllers.servo import set_servo_angle
from controllers.lighting import set_led_state

def evaluate_quality(actuate_hardware: bool = True) -> dict:
    """
    Logic for determining PASS/FAIL based on expected vs actual measurements.
    Optionally triggers hardware state based on result.
    """
    distance = read_distance()
    ir_status = read_ir_status()

    issues = []
    
    if distance > DISTANCE_MAX:
        issues.append(f"Distance {distance}cm is too far (>{DISTANCE_MAX}cm)")
        
    if ir_status != IR_EXPECTED_DETECTED:
        status_str = "detected" if ir_status else "not detected"
        expected_str = "detected" if IR_EXPECTED_DETECTED else "not detected"
        issues.append(f"IR object {status_str} (expected {expected_str})")
        
    is_pass = len(issues) == 0
    details = "PASS: All checks cleared." if is_pass else f"FAIL: {', '.join(issues)}"
    
    # --- Automation Triggers ---
    if actuate_hardware:
        if is_pass:
            set_led_state("GREEN", "ON")
            set_led_state("RED", "OFF")
            # Keep servo at default position (e.g. 0)
            set_servo_angle(0)
        else:
            set_led_state("GREEN", "OFF")
            set_led_state("RED", "ON")
            # Trigger servo to reject the object (e.g. angle 90)
            set_servo_angle(90)
    
    return {
        "is_pass": is_pass,
        "details": details,
        "measurements": {
            "weight": 0.0, # Kept for DB compatibility
            "distance": distance,
            "ir": ir_status
        }
    }
