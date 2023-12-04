from typing import Any, Dict, List
from fastapi import Body, FastAPI, Query, WebSocket

import earthaccess as ea
from src.utils import *
from src.status_handler import *
from src.download_handler import *
from src.get_data_handler import *
from src.get_file_handler import *
from pydantic import BaseModel

from http import HTTPStatus
from fastapi import BackgroundTasks
import uuid
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class Job(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    status: str = "in_progress"
    progress: int = 0
    files: list[str] = []
    data: list[str] = []

jobs: Dict[UUID, Job] = {}  # Dict as job storage
app = FastAPI()
auth = ea.login(strategy=".netrc", persist=True)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        jobKey =uuid.UUID(data)
        if jobKey in jobs:
            await websocket.send_text(f"{jobs[jobKey]}")
        else:
            await websocket.send_text("Job not available")


@app.post("/start_download", status_code=HTTPStatus.ACCEPTED)
async def start_download(background_tasks: BackgroundTasks, short_name: str | None = None, date_range: list = Query([]) , concept_id: str | None = None, bounding_box: list | None = Query(None)):
    new_job = Job()
    jobs[new_job.uid] = new_job
    background_tasks.add_task(download_handler, new_job, short_name, tuple(date_range), concept_id, tuple(bounding_box))
    return new_job.uid

@app.post("/status")
async def status(uid: UUID):
    return await status_handler(uid, jobs)

@app.post("/get_file")
async def get_file(uid: UUID):
    return await get_file_handler(uid, jobs)

@app.post("/get_data")
async def get_data(uid: UUID):
    return await get_data_handler(uid, jobs)
