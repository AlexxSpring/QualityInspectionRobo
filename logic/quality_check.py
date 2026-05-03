from sensors.loadcell import read_weight
from sensors.ultrasonic import read_distance
from sensors.ir import read_ir_status
from sys_config.thresholds import WEIGHT_MIN, WEIGHT_MAX, DISTANCE_MAX, IR_EXPECTED_DETECTED
from controllers.servo import set_servo_angle
from controllers.lighting import set_light_state

def evaluate_quality() -> dict:
    """
    Logic for determining PASS/FAIL based on expected vs actual measurements.
    Automatically triggers hardware state based on result.
    """
    weight = read_weight()
    distance = read_distance()
    ir_status = read_ir_status()

    issues = []
    
    if not (WEIGHT_MIN <= weight <= WEIGHT_MAX):
        issues.append(f"Weight {weight}kg out of tolerance ({WEIGHT_MIN}-{WEIGHT_MAX}kg)")
        
    if distance > DISTANCE_MAX:
        issues.append(f"Distance {distance}cm is too far (>{DISTANCE_MAX}cm)")
        
    if ir_status != IR_EXPECTED_DETECTED:
        status_str = "detected" if ir_status else "not detected"
        expected_str = "detected" if IR_EXPECTED_DETECTED else "not detected"
        issues.append(f"IR object {status_str} (expected {expected_str})")
        
    is_pass = len(issues) == 0
    details = "PASS: All checks cleared." if is_pass else f"FAIL: {', '.join(issues)}"
    
    # --- Automation Triggers ---
    if is_pass:
        set_light_state("ON", 100) # Full brightness for pass
        # Keep servo at default position (e.g. 0)
        set_servo_angle(0)
    else:
        # Dim light to indicate failure or switch color if RGB
        set_light_state("ON", 20) 
        # Trigger servo to reject the object (e.g. angle 90)
        set_servo_angle(90)
    
    return {
        "is_pass": is_pass,
        "details": details,
        "measurements": {
            "weight": weight,
            "distance": distance,
            "ir": ir_status
        }
    }
