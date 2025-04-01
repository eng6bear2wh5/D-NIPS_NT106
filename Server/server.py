import asyncio
import websockets
import json

async def handle_client(websocket):
    try:
        data = await websocket.recv()
        print("📩 Nhận dữ liệu mã hóa từ client...")

        packet_list = json.loads(data)  
        print(f"✅ Nhận {len(packet_list)} gói tin:")
        
        with open("captured_packets.json", "w", encoding="utf-8") as file:
            json.dump(packet_list, file, indent=4, ensure_ascii=False)
            
    except Exception as e:
        print(f"❌ Lỗi khi nhận dữ liệu: {e}")

async def main():
    async with websockets.serve(handle_client, "localhost", 8765): 
        print("🚀 Server WebSocket đang chạy trên ws://localhost:8765")
        await asyncio.Future()  

asyncio.run(main())
