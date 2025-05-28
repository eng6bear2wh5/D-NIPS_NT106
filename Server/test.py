import socket
import json
import subprocess

def block_ip_with_iptables(ip):
    try:
        cmd = ["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"]
        subprocess.run(cmd, check=True)
        print(f"[🔥] Đã block IP {ip} bằng iptables")
    except subprocess.CalledProcessError as e:
        print(f"[!] Lỗi khi chạy iptables: {e}")


# Dữ liệu JSON
data = {
    "agent": {
        "id": '3f5027a0-1d5d-49d5-b023-7cebb8e27abd',
        "hostname": "DESKTOP",
        "os": "Linux",
        "ip_addr": "127.0.1.1"
    },
    "packet": {
        "ip": {
            "src": "10.45.103.249",
            "dst": "239.255.255.250",
            "proto": 17,
            "ttl": 64,
            "id": 0,
            "flags": {
                "df": 0,
                "mf": 0
            },
            "frag_offset": 0,
            "tos": 0,
            "options": []
        },
        "udp": {
            "sport": 64988,
            "dport": 1900,
            "length": 151
        }
    },
    "flow": {
        "id": "10.45.103.249:64988-239.255.255.250:1900-UDP",
        "packet_count": 1,
        "byte_count": 179,
        "start_time": "2025-05-13T04:17:58.913772",
        "last_time": "2025-05-13T04:17:58.913772",
        "inter_packet_time": 0
    },
    "proto_layer": {
        "type": "ssdp"
    },
    "anomaly": {
        "score": -0.05504015455928857,
        "flow_score": 3,
        "detection_method": "isolation_forest"
    }
}

# Kết nối TCP
host = '127.0.0.1'
port = 9999

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        message = json.dumps(data) + '\n'
        s.sendall(message.encode('utf-8'))
        print("[+] Dữ liệu đã được gửi qua socket TCP")

        # Đợi phản hồi từ server
        response = s.recv(4096)  # 4KB buffer, chỉnh tùy theo server
        if response:
            response_data = response.decode('utf-8').strip()
            print(f"[+] Nhận phản hồi từ server: {response_data}")
            try:
                json_response = json.loads(response_data)
                if json_response.get("action") == "block_ip":
                    ip_to_block = json_response.get("ip")
                    block_ip_with_iptables(ip_to_block) 
                else:
                    print("[*] Không có lệnh block_ip")
            except json.JSONDecodeError:
                print("[!] Phản hồi không phải JSON hợp lệ")
        else:
            print("[!] Không nhận được phản hồi từ server")

except Exception as e:
    print(f"[!] Lỗi khi gửi/nhận dữ liệu: {e}")