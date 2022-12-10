from logging import getLogger
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import APIRouter, Depends, HTTPException, status

from .deps import get_client
from app.schema import DiscussionCreate, DiscussionCreateResponse
from app.service.discussion_service import DiscussionService

logger = getLogger(f'uvicorn.{__name__}')
router = APIRouter()

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=DiscussionCreateResponse)
async def create_discussion(discussion: DiscussionCreate, client: AsyncElasticsearch = Depends(get_client)):
    logger.debug(
        "[api] Attempting to create new post %s from user %s.",
        discussion.title,
        discussion.user_id
    )
    doc_id = await DiscussionService.create(client, discussion.dict())
    if doc_id:
        logger.debug("[api] Create discussion %s successful: %s", discussion.title, doc_id)
        return {"id": doc_id}

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Unable to create discussion with this info."
    )

@router.get("/get/{_id}", status_code=status.HTTP_200_OK, response_model=DiscussionCreate)
async def get_discussion(_id: str, client: AsyncElasticsearch = Depends(get_client)):
    try:
        logger.debug("[api] Attempting to retrieve discussion ID %s.", _id)
        response = await DiscussionService.get(client, _id)
    except NotFoundError as e:
        logger.debug("[api] Not found error %s", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No dicsussion with id {_id} found."
        )
    logger.debug("[api] Found discussion by user %s, title %s.",
                 response.get("user_id"), response.get("title"))
    return response

@router.post("find", status_code=status.HTTP_200_OK, response_model=DiscussionCreate)
async def find_discussion(client: AsyncElasticsearch = Depends(get_client)):
   pass