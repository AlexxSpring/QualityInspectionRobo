from fastapi import APIRouter
from pydantic import BaseModel

from controllers.servo import set_servo_angle
from controllers.lighting import set_led_state

router = APIRouter()

class ServoCommand(BaseModel):
    angle: int

class LightCommand(BaseModel):
    color: str # "GREEN" or "RED"
    state: str # "ON" or "OFF" or "TOGGLE"

@router.post("/servo")
async def control_servo(command: ServoCommand):
    set_servo_angle(command.angle)
    return {"status": "success", "angle": command.angle}

@router.post("/light")
async def control_light(command: LightCommand):
    set_led_state(command.color, command.state)
    return {"status": "success", "color": command.color, "state": command.state}
