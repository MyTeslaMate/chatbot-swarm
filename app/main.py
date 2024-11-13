# main.py
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from fastapi import FastAPI, WebSocket
from swarm import Swarm
from swarm.repl import run_demo_loop

# Import and initialize agents
from agents.base_agents import *

# Initialize FastAPI and Swarm
app = FastAPI()
swarm = Swarm()

agent = user_interface_agent
messages = []

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    global agent 
    global messages
    while True:
        data = await websocket.receive_text()
        messages.append({"role": "user", "content": data})
        response = swarm.run(agent=agent, messages=messages)
        agent = response.agent
        await websocket.send_text(pretty_print_messages(response.messages))

if __name__ == "__main__":
    run_demo_loop(user_interface_agent)
    # You can add any initialization code here
    #import uvicorn
    #uvicorn.run(app, host="0.0.0.0", port=8000)
