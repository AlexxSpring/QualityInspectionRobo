from sensors.loadcell import read_weight
from sensors.ultrasonic import read_distance
from sensors.ir import read_ir_status

def evaluate_quality() -> dict:
    """
    Mock logic for determining PASS/FAIL based on expected vs actual measurements.
    """
    weight = read_weight()
    distance = read_distance()
    ir_status = read_ir_status()

    # Dummy thresholds for MVP
    # Pass if:
    # 1. Weight is between 2.4 and 2.6 kg
    # 2. Distance is less than 20 cm
    # 3. IR sensor detects the object
    
    issues = []
    
    if not (2.4 <= weight <= 2.6):
        issues.append(f"Weight {weight}kg is out of tolerance (2.4-2.6kg)")
        
    if distance > 20.0:
        issues.append(f"Distance {distance}cm is too far (>20cm)")
        
    if not ir_status:
        issues.append("Object not detected by IR sensor")
        
    is_pass = len(issues) == 0
    details = "PASS: All checks cleared." if is_pass else f"FAIL: {', '.join(issues)}"
    
    return {
        "is_pass": is_pass,
        "details": details
    }
