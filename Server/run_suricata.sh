#!/bin/bash

REPORTS_DIR="$1"      # Thư mục chứa JSON
OUTPUT_DIR="$2"       # Thư mục lưu kết quả
PCAP_FILE="$OUTPUT_DIR/reconstructed.pcap"
SURICATA_CONFIG="/etc/suricata/suricata.yaml"
REPORT_PY="./generate_report.py"
JSON2PCAP="./json2pcap.py"

if [ -z "$REPORTS_DIR" ] || [ -z "$OUTPUT_DIR" ]; then
    echo "Usage: $0 <json_reports_dir> <output_dir>"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

# Bước 1: Chuyển đổi JSON sang PCAP
echo "Chuyển đổi JSON sang PCAP..."
python3 "$JSON2PCAP" -d "$REPORTS_DIR" -o "$PCAP_FILE"
if [ ! -f "$PCAP_FILE" ]; then
    echo "Không tạo được file PCAP!"
    exit 1
fi
echo "Đã tạo file PCAP: $PCAP_FILE"

# Bước 2: Chạy Suricata phân tích file PCAP
sudo suricata -r "$PCAP_FILE" -c "$SURICATA_CONFIG" -l "$OUTPUT_DIR"
echo "Suricata đã chạy xong. File eve.json ở: $OUTPUT_DIR/eve.json"

# Bước 3: Sinh báo cáo HTML từ eve.json
if [ -f "$OUTPUT_DIR/eve.json" ]; then
    python3 "$REPORT_PY" "$OUTPUT_DIR/eve.json" "$OUTPUT_DIR/report.html"
    echo "Đã tạo báo cáo HTML: $OUTPUT_DIR/report.html"
else
    echo "Không tìm thấy file $OUTPUT_DIR/eve.json để tạo báo cáo!"
fi