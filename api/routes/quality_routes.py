from fastapi import APIRouter
from pydantic import BaseModel
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from logic.quality_check import evaluate_quality

router = APIRouter()

class QualityResult(BaseModel):
    is_pass: bool
    details: str

@router.post("/check", response_model=QualityResult)
async def check_quality():
    # In a real scenario, this might read from sensors directly or accept sensor data as input.
    # For MVP, we'll let evaluate_quality read the dummy sensors.
    result = evaluate_quality()
    return result
