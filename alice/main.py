import os
import signal
import asyncio
import uvicorn
import functools
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat, telegram
from app.telegram import load, run


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


@app.post('/channel')
async def post_channel():
    ''' post to telegram channel '''


app.include_router(chat.router)
app.include_router(telegram.router)


async def boot_api():
    cfg = uvicorn.Config('main:app', host='127.0.0.1', port=8000, log_level='info', workers=2)
    server = uvicorn.Server(cfg)
    await asyncio.gather(
        server.serve()
    )


async def boot_tg():
    cfg = load('telegram.yml')
    await run(cfg)


async def main():
    try:
        await asyncio.gather(
            boot_api(),
            boot_tg(),
        )
    except asyncio.CancelledError as e:
        print('main() cancelled')
    except Exception as e:
        print(f'main() got: {e}')


if __name__ == '__main__':
    asyncio.run(main())
