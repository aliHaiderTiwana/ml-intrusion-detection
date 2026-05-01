from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List
import joblib
import pandas as pd
import json
import sqlite3
import datetime
import asyncio

app = FastAPI(title="Autonomous IDS SOC", version="2.0")

# --- CORS: Allow the UI to talk to the API ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DATABASE SETUP ---
DB_NAME = "security_logs.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            source_ip TEXT,
            packet_size INTEGER,
            prediction TEXT,
            raw_output INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- WEBSOCKET MANAGER ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

# --- WAKING UP THE AI ---
print("Waking up the AI...")
try:
    rf_model = joblib.load('autonomous_ids_model.pkl')
    scaler = joblib.load('ids_scaler.pkl')
    with open('model_features.json', 'r') as f:
        expected_columns = json.load(f)
    print("AI successfully loaded!")
except FileNotFoundError:
    print("CRITICAL ERROR: Could not find the .pkl files.")

class NetworkPacket(BaseModel):
    features: Dict[str, Any]
    source_ip: str = "Unknown"

# --- THE PREDICTION ENDPOINT ---
@app.post("/predict")
async def predict_traffic(packet: NetworkPacket):
    try:
        live_data = pd.DataFrame(0.0, index=[0], columns=expected_columns)
        for key, value in packet.features.items():
            if key in expected_columns:
                live_data.at[0, key] = value
                
        numeric_cols = scaler.feature_names_in_
        live_data[numeric_cols] = scaler.transform(live_data[numeric_cols])
        
        prediction = rf_model.predict(live_data)
        raw_output = int(prediction[0])
        result = "Normal" if raw_output == 6 else "Attack" # Adjust '6' based on your LabelEncoder

        # --- DATABASE LOGGING ---
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        packet_size = packet.features.get("sbytes", 0)
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO logs (timestamp, source_ip, packet_size, prediction, raw_output)
            VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, packet.source_ip, packet_size, result, raw_output))
        conn.commit()
        conn.close()

        # --- WEBSOCKET BROADCAST ---
        log_entry = {
            "timestamp": timestamp,
            "source_ip": packet.source_ip,
            "packet_size": packet_size,
            "prediction": result,
            "raw_output": raw_output
        }
        await manager.broadcast(log_entry)

        return {"status": "success", "prediction": result}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- WEBSOCKET ENDPOINT ---
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # We just need to keep the connection open
            await websocket.receive_text() 
    except WebSocketDisconnect:
        manager.disconnect(websocket)