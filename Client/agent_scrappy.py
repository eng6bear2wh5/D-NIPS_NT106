from scapy.all import sniff
import websockets
import asyncio
import json
import time

captured_data = []

def packet_callback(packet):
    try:
        if packet.haslayer("IP"):
            info = {
                "src_ip": packet["IP"].src,
                "dst_ip": packet["IP"].dst,
                "protocol": packet.proto
            }
            if packet.haslayer("TCP") or packet.haslayer("UDP"):
                info["src_port"] = packet.sport
                info["dst_port"] = packet.dport
            if packet.haslayer("Raw"):
                info["payload"] = packet["Raw"].load.hex() 
            captured_data.append(info)
    except Exception as e:
        print(f"Lỗi xử lý gói tin: {e}")

async def send_data():
    while True:
        if captured_data:
            json_data = json.dumps(captured_data)  
            while True:  
                try:
                    async with websockets.connect("ws://localhost:8765") as websocket:
                        await websocket.send(json_data)
                    captured_data.clear()
                    break  
                except Exception as e:
                    # print(f"[!] Mất kết nối, thử lại sau 5 giây... ({e})")
                    await asyncio.sleep(5) 
        await asyncio.sleep(10)  
async def main():
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, lambda: sniff(prn=packet_callback, store=False))
    await send_data()

asyncio.run(main())
