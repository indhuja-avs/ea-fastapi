async def websocket_handler(websocket, jobs):
    await websocket.accept()
    while True:
        # Receive a job_id from the WebSocket connection
        job_id = await websocket.receive_text()
        if job_id in jobs:
            await websocket.send_text(f"{jobs[job_id].status}")
        else:
            await websocket.send_text("Job not available")