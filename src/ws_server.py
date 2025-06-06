import asyncio
import websockets

connected_clients = set()

async def ws_handler(websocket, path):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            # Biz client'tan mesaj beklemiyoruz, sadece bağlantıyı tutuyoruz
            pass
    except:
        pass
    finally:
        connected_clients.remove(websocket)

async def broadcast(message):
    if connected_clients:
        await asyncio.wait([client.send(message) for client in connected_clients])

def start_ws_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    server = websockets.serve(ws_handler, "localhost", 6789)
    loop.run_until_complete(server)
    print("WebSocket server başladı: ws://localhost:6789")
    loop.run_forever()

if __name__ == "__main__":
    start_ws_server()
