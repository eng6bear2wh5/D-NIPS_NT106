import pcap
import struct
import socket
import json
import asyncio
import websockets

INTERFACES = ["eth0", "eth1", "wlan0"]  
agent_id = "d86a6d80-c0c2-4c65-a836-61a3bf86bfb3"
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
    cap = pcap.pcap(name=INTERFACES, promisc=True, immediate=True, timeout_ms=50)
    print(f"📡 Đang bắt gói tin trên interface: {INTERFACES}...")

    for ts, pkt in cap:
        packet_data = parse_packet(ts, pkt)
        if packet_data:
            async with websockets.connect(uri) as ws:
                await ws.send(json.dumps(packet_data))
                print(f"📤 Gửi gói tin: {packet_data}")
            break  # Gửi 1 gói xong thì thoát vòng lặp

# Chạy chương trình chính
if __name__ == "__main__":
    asyncio.run(send_one_packet("ws://localhost:8765"))
