from fastapi import APIRouter
from pydantic import BaseModel

from sensors.loadcell import read_weight
from sensors.ultrasonic import read_distance
from sensors.ir import read_ir_status

router = APIRouter()

class SensorData(BaseModel):
    weight_kg: float
    distance_cm: float
    ir_object_detected: bool

@router.get("", response_model=SensorData)
async def get_all_sensors():
    return {
        "weight_kg": read_weight(),
        "distance_cm": read_distance(),
        "ir_object_detected": read_ir_status()
    }
