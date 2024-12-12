import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.telegram import send_channel

'''
Routers within 'host/telegram/***'
'''

router = APIRouter(
    prefix='/telegram',
    tags=['telegram'],
    responses={404: {'description': 'Not found'}},
)


class ReqChannel(BaseModel):
    text: str
    channelId: int


@router.post('/channel')
async def chat(req :ReqChannel):
    await send_channel(req.channelId, req.text)
    return {'reply': 'OK'}
