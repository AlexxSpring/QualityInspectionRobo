from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from vision.camera import generate_frames

router = APIRouter()

@router.get("/stream")
async def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")
