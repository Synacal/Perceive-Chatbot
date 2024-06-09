from fastapi import APIRouter, HTTPException
from app.services.requirements_gathering import get_requirements_gathering
from app.models.requirements_gathering import RequirementsGathering

router = APIRouter()


@router.post("/requirements_gathering")
async def requirements_gathering(requirements: RequirementsGathering):
    try:
        response_data = await get_requirements_gathering(requirements)
        return response_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
