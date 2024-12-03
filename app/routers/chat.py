import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.ai import Gemini

'''
Routers within 'host/chat'
'''

router = APIRouter(
    prefix='/chat',
    tags=['chat'],
    responses={404: {'description': 'Not found'}},
)

api_key_gemini = os.getenv('API_KEY_GEMINI')
provider = Gemini(api_key_gemini)


class ReqChat(BaseModel):
    text: str

@router.post('/')
async def chat(req :ReqChat):
    if not req.text:
        return
    
    try:
        reply = provider.send(req.text)
    except Exception as e:
        print('Exception:', e)
        reply = ''

    return {'reply': reply}
