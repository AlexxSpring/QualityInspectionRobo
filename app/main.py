import sys
import os

# Ensure the project root is always on sys.path regardless of how uvicorn is invoked
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

from api.routes import sensor_routes, camera_routes, quality_routes, control_routes, log_routes

app = FastAPI(title="Quality Inspection Dashboard System")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Include Routers
app.include_router(sensor_routes.router, prefix="/api/sensors", tags=["Sensors"])
app.include_router(camera_routes.router, prefix="/api/camera", tags=["Camera"])
app.include_router(quality_routes.router, prefix="/api/quality", tags=["Quality"])
app.include_router(control_routes.router, prefix="/api/control", tags=["Control"])
app.include_router(log_routes.router, prefix="/api/logs", tags=["Logs"])

@app.get("/")
async def serve_dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
