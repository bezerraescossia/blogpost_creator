from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from uuid import uuid4
import asyncio
import traceback


v1_router = APIRouter()

# In-memory job storage. For production use a persistent store (Redis/DB).
JOBS: Dict[str, Dict[str, Any]] = {}


async def kickoff_job(data: dict) -> str:
    """Start a background job that runs the Crew kickoff and return an id immediately."""
    job_id = uuid4().hex
    JOBS[job_id] = {"status": "pending", "result": None, "error": None}
    loop = asyncio.get_running_loop()
    loop.create_task(_run_job_in_executor(job_id, data))
    return job_id


async def _run_job_in_executor(job_id: str, data: dict) -> None:
    JOBS[job_id]["status"] = "running"
    try:
        def blocking():
            # local import to ensure api contains runtime code
            from blogpost_creator.crew import BlogpostCreator

            crew = BlogpostCreator().crew()
            return crew.kickoff(inputs=data)

        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, blocking)
        JOBS[job_id]["status"] = "finished"
        JOBS[job_id]["result"] = result
    except Exception as exc:
        JOBS[job_id]["status"] = "failed"
        JOBS[job_id]["error"] = {"message": str(exc), "trace": traceback.format_exc()}


async def get_job_status(job_id: str) -> Dict[str, Any] | None:
    return JOBS.get(job_id)


@v1_router.post("/kickoff")
async def kickoff_endpoint(payload: dict):
    """Start Crew workflow and return an id immediately."""
    job_id = await kickoff_job(payload)
    return {"id": job_id}


@v1_router.get("/status/{job_id}")
async def status_endpoint(job_id: str):
    info = await get_job_status(job_id)
    if info is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return info


@v1_router.get("/")
async def root():
    return {"message": "Blogpost Creator API v1"}