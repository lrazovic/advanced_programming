from fastapi import FastAPI, HTTPException
from jsonrpcclient.requests import request_uuid
from fastapi import Depends
from jwtoken import get_current_user_email
import httpx
from utils import (
    endpoint_analysis,
    endpoint_fetcher,
    endpoint_persistence,
    endpoint_newspaper,
    long_post,
)
from models import NewsText, NewsFeed, UserRssFeedsDto


dummy_app = FastAPI()


@dummy_app.get("/get-user/{user_id}")
async def get_user_user_id(user_id: int):
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

@dummy_app.delete("/delete-user/{user_id}")
async def delete_user_user_id(user_id: int):
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

@dummy_app.get("/getnews")
async def dummy_fetcher_response():
    res = {
        "jsonrpc": "2.0",
        "result": {
            "Blog title": "Repubblica.it > Homepage",
            "Blog link": "https://www.repubblica.it",
            "posts": long_post,
        },
        "id": 1,
    }

    return res


@dummy_app.get("/summary")
async def dummy_summary_response():
    res = {
        "id": "c8b822b3-a40c-4472-aabf-2555f0ef073a",
        "jsonrpc": "2.0",
        "result": "Harry Potter is a series of seven fantasy novels written by British author J. K. Rowling. Since the release of the first novel, Harry Potter and the Philosopher's Stone, on 26 June 1997, the books have found immense popularity, positive reviews, and commercial success worldwide. They have attracted a wide adult audience as well as younger readers and are often considered cornerstones of modern young adult literature.",
    }

    return res


@dummy_app.post("/getnews")
async def call_fetcher(feed: NewsFeed):
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


@dummy_app.post("/summary")
async def summary(text: NewsText):
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


@dummy_app.get("/getnews")
async def dummy_call_fetcher():
    res = {
        "jsonrpc": "2.0",
        "result": {
            "Blog title": "Repubblica.it > Homepage",
            "Blog link": "https://www.repubblica.it",
            "posts": long_post,
        },
        "id": 1,
    }

    return res


@dummy_app.get("/prot/summary")
async def dummy_prot_summary(_: str = Depends(get_current_user_email)):
    res = {
        "id": "c8b822b3-a40c-4472-aabf-2555f0ef073a",
        "jsonrpc": "2.0",
        "result": "Harry Potter is a series of seven fantasy novels written by British author J. K. Rowling. Since the release of the first novel, Harry Potter and the Philosopher's Stone, on 26 June 1997, the books have found immense popularity, positive reviews, and commercial success worldwide. They have attracted a wide adult audience as well as younger readers and are often considered cornerstones of modern young adult literature.",
    }

    return res


@dummy_app.post("/get-article-detail")
async def call_newspaper(articleUrl: str):
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


@dummy_app.put("/put-user-rss-feed")
async def put_user_rss_feed(dto: UserRssFeedsDto):
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


@dummy_app.get("/readdb")
async def dummy_readdb():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                endpoint_persistence,
                json=request_uuid("read_db"),
            )
        if response.is_error:
            raise HTTPException(status_code=404, detail="Error in JSON-RPC response")
        else:
            return response.json()
    except:
        raise HTTPException(
            status_code=500, detail="Impossible to connect to JSON-RPC Server"
        )


@dummy_app.get("/prot/readdb")
async def dummy_prot_readdb(current_email: str = Depends(get_current_user_email)):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                endpoint_persistence,
                json=request_uuid("read_db"),
            )
        if response.is_error:
            raise HTTPException(status_code=404, detail="Error in JSON-RPC response")
        else:
            return current_email
    except:
        raise HTTPException(
            status_code=500, detail="Impossible to connect to JSON-RPC Server"
        )
