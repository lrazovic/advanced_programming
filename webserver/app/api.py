from fastapi import FastAPI, HTTPException
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
from models import NewsText, NewsFeed, UserRssFeedsDto

api_app = FastAPI()


@api_app.post("/getnews")
async def call_fetcher(feed: NewsFeed, _: str = Depends(get_current_user_email)):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                endpoint_fetcher,
                json=request_uuid("retrive_information", params=[feed.url, feed.limit]),
            )
        if response.is_error:
            raise HTTPException(status_code=404, detail="Error in JSON-RPC response")
        else:
            return response.json()
    except:
        raise HTTPException(
            status_code=500, detail="Impossible to connect to JSON-RPC Server"
        )


@api_app.post("/summary")
async def call_summary(text: NewsText, _: str = Depends(get_current_user_email)):
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


@api_app.post("/get-article-detail")
async def call_newspaper(articleUrl: str, _: str = Depends(get_current_user_email)):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                endpoint_newspaper,
                json=request_uuid("extract_full_text", params=[articleUrl]),
            )
        if response.is_error:
            raise HTTPException(status_code=404, detail="Error in JSON-RPC response")
        else:
            return response.json()
    except:
        raise HTTPException(
            status_code=500, detail="Impossible to connect to JSON-RPC Server"
        )


@api_app.put("/put-user-rss-feed")
async def put_user_rss_feed(
    dto: UserRssFeedsDto, _: str = Depends(get_current_user_email)
):
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

@api_app.get("/get-logged-user")
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

@api_app.delete("/delete-logged-user")
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
