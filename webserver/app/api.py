from fastapi import APIRouter, FastAPI, HTTPException
from fastapi import Depends
from jsonrpcclient.requests import request_uuid
import httpx

from jwtoken import get_current_user_email
from utils import (
    endpoint_analysis,
    endpoint_fetcher,
    endpoint_newspaper,
    endpoint_persistence,
)
from models import NewsText, UserRssFeedsDto

usersRouter = APIRouter(
    prefix="/api/users",
    tags=["users"],
    dependencies=[Depends(get_current_user_email)],
    responses={404: {"description": "Not found"}},
)

newsRouter = APIRouter(
    prefix="/api/news",
    tags=["news"],
    dependencies=[Depends(get_current_user_email)],
    responses={404: {"description": "Not found"}},
)

# -----------------------------------------------USERS

@usersRouter.get("/{user_id}")
async def get_users_user_id(user_id: int):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                endpoint_persistence,
                json=request_uuid("getUserUserId", params=[user_id]),
            )
        if response.is_error:
            raise HTTPException(status_code=404, detail="Error in JSON-RPC response")
        else:
            return response.json()
    except:
        raise HTTPException(
            status_code=500, detail="Impossible to connect to JSON-RPC Server"
        )

@usersRouter.put("/rss-feeds")
async def put_users_rss_feed(dto: UserRssFeedsDto):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                endpoint_persistence,
                json=request_uuid("update_user_rss_feeds", params=[dto.dict()]),
            )
        if response.is_error:
            raise HTTPException(status_code=404, detail="Error in JSON-RPC response")
        else:
            return response.json()
    except:
        raise HTTPException(
            status_code=500, detail="Impossible to connect to JSON-RPC Server"
        )

@usersRouter.delete("/{user_id}")
async def delete_users_user_id(user_id: int):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                endpoint_persistence,
                json=request_uuid("deleteUserUserId", params=[user_id]),
            )
        if response.is_error:
            raise HTTPException(status_code=404, detail="Error in JSON-RPC response")
        else:
            return response.json()
    except:
        raise HTTPException(
            status_code=500, detail="Impossible to connect to JSON-RPC Server"
        )

# -----------------------------------------------NEWS

@newsRouter.get("", tags=["news"])
async def call_fetcher(feed_url: str, limit: int):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                endpoint_fetcher,
                json=request_uuid("retrive_information", params=[feed_url, limit])
            )
        if response.is_error:
            raise HTTPException(status_code=404, detail="Error in JSON-RPC response")
        else:
            return response.json()
    except:
        raise HTTPException(
            status_code=500, detail="Impossible to connect to JSON-RPC Server"
        )

@newsRouter.get("/articles", tags=["news"])
async def call_newspaper(article_url: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                endpoint_newspaper,
                json=request_uuid("extract_full_text", params=[article_url])
            )
        if response.is_error:
            raise HTTPException(status_code=404, detail="Error in JSON-RPC response")
        else:
            return response.json()
    except:
        raise HTTPException(
            status_code=500, detail="Impossible to connect to JSON-RPC Server"
        )

@newsRouter.post("/articles/summary", tags=["news"])
async def call_summary(text: NewsText):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                endpoint_analysis,
                json=request_uuid(
                    "summarize",
                    params=[text.body],
                ),
            )
        if response.is_error:
            raise HTTPException(status_code=404, detail="Error in JSON-RPC response")
        else:
            return response.json()
    except:
        raise HTTPException(
            status_code=500, detail="Impossible to connect to JSON-RPC Server"
        )

# -----------------------------------------------TBD

@usersRouter.get("/get-logged-user", tags=["tbd"])
async def get_logged_user(email: str = Depends(get_current_user_email)):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                endpoint_persistence,
                json=request_uuid("getLoggedUser", params=[email]),
            )
        if response.is_error:
            raise HTTPException(status_code=404, detail="Error in JSON-RPC response")
        else:
            return response.json()
    except:
        raise HTTPException(
            status_code=500, detail="Impossible to connect to JSON-RPC Server"
        )

@usersRouter.delete("/delete-logged-user", tags=["tbd"])
async def get_logged_user(email: str = Depends(get_current_user_email)):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                endpoint_persistence,
                json=request_uuid("deleteLoggedUser", params=[email]),
            )
        if response.is_error:
            raise HTTPException(status_code=404, detail="Error in JSON-RPC response")
        else:
            return response.json()
    except:
        raise HTTPException(
            status_code=500, detail="Impossible to connect to JSON-RPC Server"
        )
