import asyncio
import websockets

CONNECTIONS = set()

async def handler(websocket):
    CONNECTIONS.add(websocket)
    try:
        async for message in websocket:
            for conn in CONNECTIONS:
                if conn != websocket:
                    await conn.send(message)
    finally:
        CONNECTIONS.remove(websocket)

async def main():
    async with websockets.serve(handler, "localhost", 8181):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
