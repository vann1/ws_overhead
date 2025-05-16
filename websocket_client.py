import asyncio
import json
import time
import websockets
import os

async def send_requests():
    uri = "ws://127.0.0.1:5000"
    # Clear overhead.txt if it exists
    file_path = "overhead.txt"
    if os.path.exists(file_path):
        os.remove(file_path)
    async with websockets.connect(uri) as websocket:
        for i in range(1000):
            timestamp = time.time()
            message = json.dumps({"action": "home", "timestamp": timestamp})
            try:
                await websocket.send(message)
                response = await websocket.recv()
                print(f"Received: {response}")
            except websockets.exceptions.ConnectionClosed:
                print("Connection closed")
                break
            except Exception as e:
                print(f"Error: {e}")
                break

if __name__ == "__main__":
    asyncio.run(send_requests())