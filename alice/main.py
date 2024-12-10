import os
import signal
import asyncio
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat

origins = [
    'http://localhost:3000',
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    print('shutdown')
    os.kill(os.getpid(), signal.SIGTERM)


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/')
async def test():
    return {'msg': 'passed'}


app.include_router(chat.router)


async def main():
    cfg = uvicorn.Config('main:app', host='127.0.0.1', port=8000, log_level='info', workers=2)
    server = uvicorn.Server(cfg)
    await asyncio.gather(
        server.serve()
    )


if __name__ == '__main__':
    asyncio.run(main())
