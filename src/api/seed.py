from fastapi import APIRouter
from seed_scripts import seed


router = APIRouter(prefix="/seed")

@router.post("/")
async def execute_seed_script():
    await seed()
    return {"status": "success"}
