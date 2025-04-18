import socket
import pcap
import platform
import psutil
import datetime
import psycopg2
import uuid
import asyncio
import websockets
import json
import signal
import datetime


INTERFACE = "eth0"  
agent_id = str(uuid.uuid4())

def update_agent_last_seen(agent_id):
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        os = platform.system()  
        status = "active" if psutil.boot_time() else "inactive"
        current_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
        # agent_name = get_latest_agent_name() + 1
        conn = psycopg2.connect("postgres://avnadmin:AVNS_-KEo1AvB98NH557DB5v@pg-18c83e66-d-nips.d.aivencloud.com:20242/mydb?sslmode=require")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO public."AGENTS" ("ID", "LAST_SEEN", "HOSTNAME", "IP_ADDRESS", "OS", "STATUS")
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (agent_id, current_time, hostname, ip_address, os, status))
    
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Lỗi cập nhật AGENT: {e}")


def parse_packet(ts, pkt):
    eth_length = 14

    # Kiểm tra độ dài gói tin
    # if len(pkt) < eth_length + 20:
    #     return None

    # ip_header = pkt[eth_length:eth_length + 20]
    # iph = struct.unpack('!BBHHHBBH4s4s', ip_header)

    # protocol_num = iph[6]
    # protocol = {6: "TCP", 17: "UDP"}.get(protocol_num, "Other")

    # src_ip = socket.inet_ntoa(iph[8])
    # dst_ip = socket.inet_ntoa(iph[9])

    # src_port = dst_port = None
    # if protocol in ["TCP", "UDP"]:
    #     ip_header_len = (iph[0] & 0x0F) * 4
    #     tcp_udp_offset = eth_length + ip_header_len
    #     ports = struct.unpack('!HH', pkt[tcp_udp_offset:tcp_udp_offset + 4])
    #     src_port, dst_port = ports

    return {
        # "src_ip": src_ip,
        # "dst_ip": dst_ip,
        # "src_port": src_port,
        # "dst_port": dst_port,
        # "protocol": protocol,
        # "size": len(pkt),
        # "suspicious_ai": "Yes"  # Gắn nhãn giả lập AI

        "agent_id": agent_id,
        "src_ip": "172.25.0.1",
        "dst_ip": "224.0.0.251",
        "src_port": 5353,
        "dst_port": 5353,
        "protocol": "UDP",
        "size": 408,
        "suspicious_ai": "Yes"
        
    }

async def send_one_packet(uri):
    cap = pcap.pcap(name=INTERFACE, promisc=True, immediate=True, timeout_ms=50)
    print(f"📡 Đang bắt gói tin trên interface: {INTERFACE}...")

    for ts, pkt in cap:
        packet_data = parse_packet(ts, pkt)
        if not packet_data:
            continue

        while True:
            try:
                async with websockets.connect(uri) as ws:
                    await ws.send(json.dumps(packet_data))
                    print(f"📤 Gửi gói tin: {packet_data}")
                    break  # Gửi thành công thì thoát vòng lặp reconnect
            except Exception as e:
                print(f"⚠️ Lỗi kết nối WebSocket: {e}")
                print("🔄 Thử reconnect sau 5 giây...")
                await asyncio.sleep(5)
        break  

async def main():
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, lambda: asyncio.create_task(shutdown(loop)))
    # await send_one_packet("ws://localhost:8765")

async def shutdown(loop):
    print("Đang dừng chương trình...")
    loop.stop()  # Dừng vòng lặp asyncio



if __name__ == "__main__":
    update_agent_last_seen(agent_id)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # print("Đã nhận tín hiệu Ctrl+C. Kết thúc chương trình.")
        exit(0)
