from fastapi import FastAPI, HTTPException
from fastapi import Depends
from jsonrpcclient.requests import request_uuid

import httpx

from jwtoken import get_current_user_email
from utils import endpoint_analysis, endpoint_fetcher

api_app = FastAPI()


@api_app.get("/getnews")
async def call_fetcher():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                endpoint_fetcher,
                json=request_uuid("retrive_information"),
            )
        if response.is_error:
            raise HTTPException(status_code=404, detail="Error in JSON-RPC response")
        else:
            return response.json()
    except:
        raise HTTPException(
            status_code=500, detail="Impossible to connect to JSON-RPC Server"
        )


@api_app.get("/summary")
async def summary(current_email: str = Depends(get_current_user_email)):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                endpoint_analysis,
                json=request_uuid(
                    "summarize",
                    params=[
                        "Harry Potter is a series of seven fantasy novels written by British author J. K. Rowling."
                    ],
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
