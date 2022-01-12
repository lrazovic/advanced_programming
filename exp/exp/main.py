from fastapi import FastAPI
from easyauth.server import EasyAuthServer

app = FastAPI()

@app.on_event('startup')
async def startup():
    app.auth = await EasyAuthServer.create(
        app, 
        '/auth/token',
        auth_secret='abcd1234',
        admin_title='Hello Secured World',
        admin_prefix='/admin',
        env_from_file='/home/ai/WIP/labAP/advanced_programming/exp/server_sqlite.json'
    )

    @app.auth.get('/')
    async def hello_world():
        return "Hello World!"