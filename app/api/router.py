from logging import getLogger
from elasticsearch import AsyncElasticsearch
from fastapi import APIRouter, Depends, HTTPException, status

from .deps import get_client, get_current_user
from app.schema import Discussion, DiscussionCreate, DiscussionCreateResponse, DiscussionSearchResponse
from app.service.discussion_service import DiscussionService

logger = getLogger(f'uvicorn.{__name__}')
router = APIRouter()

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=DiscussionCreateResponse)
async def create_discussion(discussion: DiscussionCreate,
                            user: dict = Depends(get_current_user),
                            client: AsyncElasticsearch = Depends(get_client)):
    # TODO: Move user schema to a common place
    logger.debug(
        "[api] Attempting to create new post %s from user %s.",
        discussion.title,
        user.get("email")
    )
    doc_dict = discussion.dict()
    doc_dict["user_id"] = user.get("email")
    doc_id = await DiscussionService.create(client, doc_dict)
    if doc_id:
        logger.debug("[api] Create discussion %s successful: %s", discussion.title, doc_id)
        return {"id": doc_id}

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Unable to create discussion with this info."
    )

@router.get("/search", status_code=status.HTTP_200_OK, response_model=list[DiscussionSearchResponse])
async def search_discussion(query: str, client: AsyncElasticsearch = Depends(get_client)):
    logger.debug("[api] Searching with query string %s.", query)
    response = await DiscussionService.search(client, query_str=query, fields=['title^2', 'content'])
    logger.debug("[api] Found %s matching documents.", len(response))
    return response

@router.get("/{_id}", status_code=status.HTTP_200_OK, response_model=Discussion)
async def get_discussion(_id: str, client: AsyncElasticsearch = Depends(get_client)):
    logger.debug("[api] Attempting to retrieve discussion ID %s.", _id)
    response = await DiscussionService.get(client, _id)
    if response is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No dicsussion with id {_id} found."
        )
    logger.debug("[api] Found discussion by user %s, title %s.",
                 response.get("user_id"), response.get("title"))
    return response
