from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

from api import api_app
from auth import auth_app
from dummy import dummy_app

api_gateway = FastAPI()
api_gateway.mount("/auth", auth_app)
api_gateway.mount("/api", api_app)
api_gateway.mount("/dummy", dummy_app)

# Allow CORS for all origins
api_gateway.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api_gateway.get("/")
async def root():
    return HTMLResponse('<body><a href="/auth/login">Log In</a></body>')


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
            <title>Document</title>
            </head>

            <body>
            <script>
                function send() {
                var req = new XMLHttpRequest();
                req.onreadystatechange = function () {
                    if (req.readyState === 4) {
                    console.log(req.response);
                    if (req.response["result"] === true) {
                        window.localStorage.setItem("jwt", req.response["access_token"]);
                        window.localStorage.setItem(
                        "refresh",
                        req.response["refresh_token"]
                        );
                    }
                    }
                };
                req.withCredentials = true;
                req.responseType = "json";
                req.open(
                    "get",
                    "/auth/token?" + window.location.search.substr(1),
                    true
                );
                req.send("");
                }
            </script>
            <button onClick="send()">Get FastAPI JWT Token</button>

            <button onClick='fetch("dummy/getnews").then(
                        (r)=>r.json()).then((msg)=>{console.log(msg)});'>
                Call Unprotected API
            </button>
            <button onClick='fetch("dummy/prot/summary").then(
                        (r)=>r.json()).then((msg)=>{console.log(msg)});'>
                Call Protected API without JWT
            </button>
            <button onClick='fetch("dummy/prot/summary",{
                        headers:{
                            "Authorization": "Bearer " + window.localStorage.getItem("jwt")
                        },
                    }).then((r)=>r.json()).then((msg)=>{console.log(msg)});'>
                Call Protected API wit JWT
            </button>
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
