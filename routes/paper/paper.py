import json, asyncio
from datetime import timedelta
from bson import ObjectId
from fastapi import APIRouter, Response, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from config.db import paper_collection
from models.paper import SamplePaperModel
from config.cache import redis_client

router = APIRouter(tags=["Paper"])

def serialize_paper(paper):
    if "_id" in paper:
        paper["_id"] = str(paper["_id"])
    return paper

@router.get("/papers/search")
async def search_papers(query: str = Query(..., min_length=1)):
    try:
        # Full-text search on 'sections.questions.question' and 'sections.questions.answer'
        results = await paper_collection.find(
            {"$text": {"$search": query}},
            {"score": {"$meta": "textScore"}} 
        ).sort([("score", {"$meta": "textScore"})]).to_list(length=2) 
        
        if not results:
            raise HTTPException(status_code=404, detail="No matching questions found.")
        
        results = [serialize_paper(paper) for paper in results]

        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/papers/{paper_id}")
async def papers(paper_id: str):
    try:
        paper_object_id = ObjectId(paper_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid paper ID format.")
    
    cached_paper = await asyncio.to_thread(redis_client.get, paper_id) 
    if cached_paper:
        return json.loads(cached_paper)
    
    paper = await paper_collection.find_one({"_id": paper_object_id})
    if paper is None:
        raise HTTPException(status_code=404, detail="Paper not found.")    
    paper["_id"] = str(paper["_id"])

    await asyncio.to_thread(redis_client.setex, paper_id, timedelta(minutes=10), json.dumps(paper))
    return paper

@router.post("/papers")
async def papers(paper: SamplePaperModel):
    paper = jsonable_encoder(paper)
    result = await paper_collection.insert_one(paper)
    return JSONResponse(status_code=201, content={"paper_id": str(result.inserted_id)})

@router.put("/papers/{paper_id}")
async def papers(paper_id: str, paper: SamplePaperModel):
    try:
        paper_object_id = ObjectId(paper_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid paper ID format.")
    paper = jsonable_encoder(paper)
    updated_paper = await paper_collection.update_one({"_id": paper_object_id}, {"$set": paper})
    if updated_paper.matched_count == 0:
        raise HTTPException(status_code=404, detail="Paper not found.")
    return Response(status_code=204)

@router.delete("/papers/{paper_id}")
async def papers(paper_id: str):
    try:
        paper_object_id = ObjectId(paper_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid paper ID format.")
    deleted_paper = await paper_collection.delete_one({"_id": paper_object_id})
    if deleted_paper.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Paper not found.")
    return Response(status_code=204)