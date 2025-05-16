import asyncio
import json
import time
import websockets
from websockets.exceptions import ConnectionClosed

class WebSocketServer:
    def __init__(self):
        self.counter = 0

    async def handle_connection(self, websocket, path=""):
        try:
            async for message in websocket:
                # Parse incoming JSON message
                try:
                    data = json.loads(message)
                    action = data.get("action")
                    timestamp = data.get("timestamp") # might need time.time()
                except json.JSONDecodeError:
                    await websocket.send(json.dumps({"error": "Invalid JSON"}))
                    continue

                # Log timestamp to file for overhead measurement
                server_timestamp = time.time()
                try:
                    with open("overhead.txt", "a") as file:
                        file.write(f"{timestamp}|{server_timestamp}\n")
                except IOError:
                    print("Error writing to file")

                # Handle different actions
                if action == "home":
                    self.counter += 1
                    print(f"counter: {self.counter} timestamp: {server_timestamp}")
                    response = {
                        "message": "Welcome to the WebSocket API",
                        "status": "success",
                        "counter": self.counter
                    }
                elif action == "get_item":
                    item_id = data.get("item_id")
                    if not isinstance(item_id, int):
                        response = {"error": "Invalid item_id"}
                    else:
                        await asyncio.sleep(0.1)  # Simulate async DB fetch
                        response = {
                            "item_id": item_id,
                            "name": f"Item {item_id}",
                            "status": "found"
                        }
                elif action == "create_item":
                    name = data.get("name")
                    if not name:
                        response = {"error": "Name is required"}
                    else:
                        await asyncio.sleep(0.1)  # Simulate async DB save
                        response = {
                            "message": "Item created",
                            "name": name,
                            "status": "success"
                        }
                elif action == "update_item":
                    item_id = data.get("item_id")
                    name = data.get("name")
                    if not name or not isinstance(item_id, int):
                        response = {"error": "Name and valid item_id required"}
                    else:
                        await asyncio.sleep(0.1)  # Simulate async DB update
                        response = {
                            "item_id": item_id,
                            "name": name,
                            "message": "Item updated",
                            "status": "success"
                        }
                elif action == "delete_item":
                    item_id = data.get("item_id")
                    if not isinstance(item_id, int):
                        response = {"error": "Invalid item_id"}
                    else:
                        await asyncio.sleep(0.1)  # Simulate async DB delete
                        response = {
                            "item_id": item_id,
                            "message": "Item deleted",
                            "status": "success"
                        }
                else:
                    response = {"error": "Unknown action"}

                # Send response back to client
                await websocket.send(json.dumps(response))

        except ConnectionClosed:
            print("Client disconnected")

async def run_server():
    server = WebSocketServer()
    # Ensure the handler is passed correctly
    async with websockets.serve(server.handle_connection, "127.0.0.1", 5000):
        print("WebSocket server running on ws://127.0.0.1:5000")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        print("Server stopped")