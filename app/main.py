from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import chat

origins = [
    'http://localhost:3000',
]
app = FastAPI()

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
