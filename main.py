from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, HTTPException
from bson import ObjectId
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

mongodb = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    atlas_uri = os.getenv("MONGODB_URI")
    
    print(f"DEBUG - Current Working Directory: {os.getcwd()}")
    if not atlas_uri:
        raise ValueError("CRITICAL ERROR: MONGO_URI is None. The .env file is not being read!")

    mongodb["client"] = AsyncIOMotorClient(atlas_uri)
    mongodb["db"] = mongodb["client"].techsphere
    yield
    mongodb["client"].close()

app = FastAPI(lifespan=lifespan, title="TechSphere API")

@app.get("/")
async def root():
    return {"message": "Welcome to the TechSphere API!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProjectData(BaseModel):
    title: str
    status: str

@app.post("/api/projects", response_model=ProjectData)
async def create_project(project: ProjectData):
    new_project = await mongodb["db"].projects.insert_one(project.model_dump())
    if not new_project.inserted_id:
        raise HTTPException(status_code=400, detail="Failed to create project")
    return project

@app.get("/api/projects")
async def get_projects():
    projects_cursor = mongodb["db"].projects.find({}, {"_id": 0})
    projects = await projects_cursor.to_list(length=100)
    return {"projects": projects}

@app.websocket("/ws/realtime")
async def real_time_delivery(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Server processed live event: {data}")
    except Exception:
        print("Client disconnected from real-time stream.")

@app.put("/api/projects/{project_id}")
async def update_project(project_id: str, project: ProjectData):
    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid project ID format")
    
    result = await mongodb["db"].projects.update_one(
        {"_id": ObjectId(project_id)},
        {"$set": project.model_dump()}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Project not found or no changes made")
        
    return {"message": "Project updated successfully"}

@app.delete("/api/projects/{project_id}")
async def delete_project(project_id: str):
    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid project ID format")
        
    result = await mongodb["db"].projects.delete_one({"_id": ObjectId(project_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
        
    return {"message": "Project deleted successfully"}