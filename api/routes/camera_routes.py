from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from vision.camera import generate_frames

router = APIRouter()

@router.get("/stream")
async def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")
