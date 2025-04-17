import asyncio
import websockets
import json
import psycopg2
import uuid
import time
from collections import defaultdict
import re
from rules_engine import check_rules

# PostgreSQL connection info
conn = psycopg2.connect("postgres://avnadmin:AVNS_-KEo1AvB98NH557DB5v@pg-18c83e66-d-nips.d.aivencloud.com:20242/mydb?sslmode=require")
cursor = conn.cursor()

def insert_packet(data):
    cursor.execute("""
        INSERT INTO public."PACKETS" (
            "ID", "TIMESTAMP", "PROTOCOL", "SOURCE_IP", "DEST_IP", 
            "SOURCE_PORT", "DEST_PORT", "PAYLOAD", "AGENT_ID"
        ) VALUES (
            uuid_generate_v4(), now(), %s, %s, %s, %s, %s, %s, %s
        )
    """, (
        data.get("protocol"),
        data.get("src_ip"),
        data.get("dst_ip"),
        data.get("src_port"),
        data.get("dst_port"),
        json.dumps(data),
        data.get("agent_id")
    ))
    conn.commit()

async def handle_client(websocket):
    try:
        data = await websocket.recv()
        print("\U0001F4E9 Nhận packet:")
        packet = json.loads(data)
        print(json.dumps(packet, indent=2))

        # Check rules
        alerts = check_rules(packet)
        for alert in alerts:
            print(f"⚠️ Alert (SID {alert['sid']}): {alert['msg']} from {alert['src_ip']}")
            # insert_alert(alert)  # bạn đã có hàm này để ghi vào DB
        insert_packet(packet)

    except Exception as e:
        print(f"\u274C Lỗi: {e}")

async def main():
    async with websockets.serve(handle_client, "0.0.0.0", 8765):
        print("\U0001F680 Server đang chạy tại ws://0.0.0.0:8765")
        await asyncio.Future()

asyncio.run(main())
