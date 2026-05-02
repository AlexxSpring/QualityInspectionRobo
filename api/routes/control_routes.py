from fastapi import APIRouter
from pydantic import BaseModel
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from controllers.servo import set_servo_angle
from controllers.lighting import set_light_state

router = APIRouter()

class ServoCommand(BaseModel):
    angle: int

class LightCommand(BaseModel):
    state: str # "ON" or "OFF"
    brightness: int = 100

@router.post("/servo")
async def control_servo(command: ServoCommand):
    set_servo_angle(command.angle)
    return {"status": "success", "angle": command.angle}

@router.post("/light")
async def control_light(command: LightCommand):
    set_light_state(command.state, command.brightness)
    return {"status": "success", "state": command.state, "brightness": command.brightness}
