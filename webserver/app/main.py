from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

from utils import tags_metadata

from api import usersRouter, newsRouter
from auth import auth_app

api_gateway = FastAPI(openapi_tags=tags_metadata)
api_gateway.include_router(usersRouter)
api_gateway.include_router(newsRouter)

# Sub-applications
api_gateway.mount("/auth", auth_app)

# Allow CORS for all origins
api_gateway.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api_gateway.get("/token")
async def token(request: Request):
    return HTMLResponse(
        """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <meta http-equiv="X-UA-Compatible" content="IE=edge" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>oAUth Redirect</title>
        </head>

        <body onload="send();">
            <script>
            function send() {
                var req = new XMLHttpRequest();
                req.onreadystatechange = function () {
                if (req.readyState === 4) {
                    if (req.response["result"] === true) {
                    window.localStorage.setItem("user_id", req.response["user_id"]);
                    window.localStorage.setItem("jwt", req.response["access_token"]);
                    window.localStorage.setItem(
                        "refresh",
                        req.response["refresh_token"]
                    );
                    window.close();
                    }
                }
                };
                req.withCredentials = true;
                req.responseType = "json";
                req.open(
                "get",
                "/auth/token?" + window.location.search.substring(1),
                true
                );
                req.send("");
            }
            </script>
        </body>
        </html>
        """
    )


if __name__ == "__main__":
    if "DEV" in os.environ:
        PORT = 8080
    else:
        PORT = 5000
    uvicorn.run(api_gateway, host="0.0.0.0", port=PORT)
