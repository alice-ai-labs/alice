import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.telegram import send_channel, send_group

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
    id: int


@router.post('/channel')
async def post_channel_msg(req :ReqChannel):
    await send_channel(req.id, req.text)
    return {'reply': 'OK'}


@router.post('/group')
async def post_group_msg(req :ReqChannel):
    await send_group(req.id, req.text)
    return {'reply': 'OK'}
