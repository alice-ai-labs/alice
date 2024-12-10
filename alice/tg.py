import asyncio 
from app.telegram import load, start
from app.telegram.const import Greetings


async def main():
    c = load('telegram.yml')
    token = c['bots'][0]['token']

    await start(token)

if __name__ == '__main__':
    asyncio.run(main())
