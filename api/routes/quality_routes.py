from fastapi import APIRouter
from pydantic import BaseModel

from logic.quality_check import evaluate_quality
from logic.database import log_inspection

router = APIRouter()

class QualityResult(BaseModel):
    is_pass: bool
    details: str
    measurements: dict

@router.post("/check", response_model=QualityResult)
async def check_quality():
    result = evaluate_quality()
    
    # Log the inspection to the database
    log_inspection(
        weight_kg=result["measurements"]["weight"],
        distance_cm=result["measurements"]["distance"],
        ir_detected=result["measurements"]["ir"],
        is_pass=result["is_pass"],
        details=result["details"]
    )
    
    return result
