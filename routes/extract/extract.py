from fastapi import APIRouter
from celery.result import AsyncResult
from fastapi import UploadFile, HTTPException

from worker import celery, process_text_extraction
from config.cache import redis_client

router = APIRouter(tags=["Extract"])

allowed_file_types = ["text/plain", "application/pdf"]

@router.post("/extract/pdf")
@router.post("/extract/text")
async def extract_text_from_file(file: UploadFile):
    if file.content_type not in allowed_file_types:
        raise HTTPException(status_code=400, detail="Invalid file type")
    text_data = await file.read()
    task = process_text_extraction.delay(file.content_type, text_data)
    redis_client.set(task.id, "Processing")

    return {"task_id": task.id}

@router.get("/task/{task_id}")
async def get_task_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery)
    status = redis_client.get(task_id)

    if not status:
        raise HTTPException(status_code=404, detail="Task not found")
    

    if task_result.state == 'SUCCESS':
        redis_client.set(task_id, "Completed")
        return {"task_id": task_id, "status": "Completed", "paper_id": task_result.result}
    else:
        return {"task_id": task_id, "status": task_result.state}
