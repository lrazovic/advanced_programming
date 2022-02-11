from fastapi import FastAPI, HTTPException
from fastapi import Depends
from jsonrpcclient.requests import request_uuid
import httpx

from jwtoken import get_current_user_email
from utils import endpoint_analysis, endpoint_fetcher, endpoint_newspaper
from models import NewsText, NewsFeed

api_app = FastAPI()


@api_app.post("/getnews")
async def call_fetcher(
    feed: NewsFeed, current_email: str = Depends(get_current_user_email)
):
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
async def call_summary(
    text: NewsText, current_email: str = Depends(get_current_user_email)
):
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
async def call_newspaper(
    articleUrl: str, current_email: str = Depends(get_current_user_email)
):
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
