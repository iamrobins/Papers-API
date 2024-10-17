import asyncio
from celery import Celery
from config import settings
from config.db import paper_collection
from routes.extract.utils import generate_sample_paper

celery = Celery("tasks", broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}", backend=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}")

async def insert_sample_paper_async(sample_paper):
    """Async function to insert data into MongoDB."""
    result = await paper_collection.insert_one(sample_paper)
    return result.inserted_id

@celery.task(bind=True)
def process_text_extraction(self, file_type, file_data: bytes):
    try:
        sample_paper = generate_sample_paper(file_type, file_data)

        def syncfunc():
            async def asyncfunc():
                inserted_id = await insert_sample_paper_async(sample_paper)
                return inserted_id

            return asyncio.run(asyncfunc())

        inserted_id = syncfunc()

        return str(inserted_id)

    except Exception as e:
        print(f"Error processing task: {e}")
        return None

celery.conf.update(task_routes={
    'worker.process_pdf_task': {'queue': 'celery'}
})