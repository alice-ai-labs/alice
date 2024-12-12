import asyncio
from app.telegram import load, run


async def main():
    cfg = load('telegram.yml')
    await run(cfg)


if __name__ == '__main__':
    asyncio.run(main())
