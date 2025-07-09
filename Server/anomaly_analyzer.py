#!/usr/bin/env python3
"""
Công cụ phân tích bất thường mạng tự động hóa:
- Chạy json2pcap.py để chuyển JSON thành PCAP
- Chạy suricata_analyzer.py để phân tích PCAP
- Tạo báo cáo HTML đơn giản
"""

import os
import sys
import json
import argparse
import subprocess
import logging
import shutil
from datetime import datetime
import matplotlib.pyplot as plt
import jinja2

# Thiết lập logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("AnomalyAnalyzer")

# Chạy json2pcap.py
def run_json2pcap(json2pcap_path, reports_dir, output_file, date=None, flow_id=None, recursive=True):
    """Chạy công cụ json2pcap để chuyển đổi báo cáo JSON thành PCAP"""
    logger.info("Chạy công cụ json2pcap để chuyển đổi báo cáo JSON thành PCAP...")
    
    if not os.path.exists(json2pcap_path):
        logger.error(f"Không tìm thấy công cụ json2pcap: {json2pcap_path}")
        return None
    
    cmd = [sys.executable, json2pcap_path, "-d", reports_dir, "-o", output_file]
    
    if date:
        cmd.extend(["--date", date])
    
    if flow_id:
        cmd.extend(["--flow-id", flow_id])
    
    if not recursive:
        cmd.append("--no-recursive")
    
    try:
        logger.info(f"Thực thi lệnh: {' '.join(cmd)}")
        process = subprocess.run(cmd, capture_output=True, text=True)
        
        if process.returncode != 0:
            logger.error(f"Lỗi khi chạy json2pcap: {process.stderr}")
            return None
        
        # Kiểm tra file đã được tạo hay chưa
        if not os.path.exists(output_file):
            logger.error(f"File đầu ra không được tạo: {output_file}")
            return None
            
        logger.info(f"Đã tạo thành công file PCAP: {output_file}")
        return output_file
    
    except Exception as e:
        logger.error(f"Lỗi khi chạy json2pcap: {e}")
        return None

# Chạy suricata_analyzer.py
def run_suricata_analyzer(suricata_analyzer_path, pcap_file, output_dir, 
                         suricata_bin="suricata", config_file=None, rules_dir=None):
    logger.info("Chạy công cụ suricata_analyzer để phân tích PCAP...")
    
    if not os.path.exists(suricata_analyzer_path):
        logger.error(f"Không tìm thấy công cụ suricata_analyzer: {suricata_analyzer_path}")
        return None
    
    if not os.path.exists(pcap_file):
        logger.error(f"Không tìm thấy file PCAP: {pcap_file}")
        return None
    
    # Tạo thư mục đầu ra nếu chưa tồn tại
    os.makedirs(output_dir, exist_ok=True)
    
    cmd = [sys.executable, suricata_analyzer_path, pcap_file, "-o", output_dir, "-s", suricata_bin]
    if config_file:
        cmd.extend(["-c", config_file])
    if rules_dir:
        if rules_dir.endswith('.rules'):
            cmd.extend(["-S", rules_dir])
        else:
            cmd.extend(["-r", rules_dir])
    
    try:
        logger.info(f"Thực thi lệnh: {' '.join(cmd)}")
        process = subprocess.run(cmd, capture_output=True, text=True)
        
        if process.returncode != 0:
            logger.error(f"Lỗi khi chạy suricata_analyzer: {process.stderr}")
            return None
        
        # Kiểm tra file eve.json
        eve_json = os.path.join(output_dir, "eve.json")
        if os.path.exists(eve_json):
            logger.info(f"Đã phân tích thành công file PCAP, kết quả: {eve_json}")
            return eve_json
        else:
            logger.warning(f"Không tìm thấy file kết quả eve.json sau khi phân tích")
            return None
    
    except Exception as e:
        logger.error(f"Lỗi khi chạy suricata_analyzer: {e}")
        return None

# Phân tích eve.json
def parse_eve_json(eve_json):
    """Phân tích file eve.json và trả về các cảnh báo"""
    if not eve_json or not os.path.exists(eve_json):
        logger.error(f"File eve.json không tồn tại: {eve_json}")
        return []
        
    alerts = []
    
    try:
        # Đọc file eve.json dòng theo dòng (vì nó không phải là JSON hợp lệ)
        with open(eve_json, 'r') as f:
            for line in f:
                try:
                    event = json.loads(line.strip())
                    
                    # Chỉ lọc các sự kiện alert
                    if event.get("event_type") == "alert":
                        alerts.append(event)
                
                except json.JSONDecodeError:
                    continue
        
        return alerts
    
    except Exception as e:
        logger.error(f"Lỗi khi đọc file eve.json: {e}")
        return []

# Tạo biểu đồ tóm tắt cảnh báo
def create_suricata_summary_chart(alerts, output_file="suricata_summary.png"):
    """Tạo biểu đồ tóm tắt cảnh báo Suricata"""
    if not alerts:
        logger.warning("Không có cảnh báo Suricata để tạo biểu đồ.")
        return None
    
    # Tổng hợp dữ liệu theo loại cảnh báo
    categories = {}
    severity_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    
    for alert in alerts:
        category = alert.get("alert", {}).get("category", "Unknown")
        categories[category] = categories.get(category, 0) + 1
        
        severity = alert.get("alert", {}).get("severity", 0)
        if severity in severity_counts:
            severity_counts[severity] += 1
    
    # Sắp xếp và giới hạn top 5 loại cảnh báo
    top_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Tạo biểu đồ
    plt.figure(figsize=(12, 10))
    
    # Biểu đồ phân loại cảnh báo
    plt.subplot(2, 1, 1)
    cat_names = [cat for cat, _ in top_categories]
    cat_values = [val for _, val in top_categories]
    
    plt.bar(cat_names, cat_values, color='orange')
    plt.title('Top 5 loại cảnh báo Suricata')
    plt.ylabel('Số lượng cảnh báo')
    plt.xticks(rotation=45, ha='right')
    
    # Biểu đồ mức độ nghiêm trọng
    plt.subplot(2, 1, 2)
    severity_names = ["Rất thấp", "Thấp", "Trung bình", "Cao", "Rất cao"]
    severity_values = list(severity_counts.values())
    
    colors = ['green', 'lightgreen', 'yellow', 'orange', 'red']
    plt.bar(severity_names, severity_values, color=colors)
    plt.title('Phân bố mức độ nghiêm trọng')
    plt.ylabel('Số lượng cảnh báo')
    
    plt.tight_layout()
    
    # Lưu biểu đồ
    plt.savefig(output_file)
    logger.info(f"Đã lưu biểu đồ tóm tắt Suricata vào: {output_file}")
    return output_file

# Tạo báo cáo HTML đơn giản
def create_html_report(pcap_file, suricata_alerts, suricata_chart=None, output_dir="./report"):
    """Tạo báo cáo HTML đơn giản"""
    # Tạo thư mục output nếu chưa tồn tại
    os.makedirs(output_dir, exist_ok=True)
    
    # Tạo thư mục assets cho hình ảnh
    assets_dir = os.path.join(output_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    
    # Copy biểu đồ vào thư mục assets
    chart_path = None
    if suricata_chart and os.path.exists(suricata_chart):
        dest_file = os.path.join(assets_dir, os.path.basename(suricata_chart))
        shutil.copy2(suricata_chart, dest_file)
        chart_path = f"assets/{os.path.basename(suricata_chart)}"
    
    # Chuẩn bị dữ liệu cho template
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    template_data = {
        "title": "Báo cáo phân tích bất thường mạng",
        "date": today,
        "pcap_file": os.path.basename(pcap_file) if pcap_file else "Không có",
        "suricata_alerts": suricata_alerts,
        "chart_path": chart_path,
    }
    
    # Mẫu HTML đơn giản
    template_str = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        .section {
            margin-bottom: 40px;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 20px;
            background-color: #f9f9f9;
        }
        .chart {
            text-align: center;
            margin: 20px 0;
        }
        .chart img {
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-shadow: 0 0 5px rgba(0,0,0,0.2);
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            padding: 12px 15px;
            border: 1px solid #ddd;
            text-align: left;
        }
        th {
            background-color: #3498db;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        .severity-high {
            color: #e74c3c;
            font-weight: bold;
        }
        .severity-medium {
            color: #f39c12;
        }
        .severity-low {
            color: #27ae60;
        }
        footer {
            text-align: center;
            margin-top: 50px;
            padding-top: 10px;
            border-top: 1px solid #ddd;
            color: #7f8c8d;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>{{ title }}</h1>
        <p>Ngày tạo báo cáo: {{ date }}</p>
    </div>
    
    <div class="section">
        <h2>Thông tin PCAP</h2>
        <p>File PCAP: {{ pcap_file }}</p>
    </div>
    
    <div class="section">
        <h2>Phân tích Suricata</h2>
        
        {% if suricata_alerts %}
        <h3>Tổng quan</h3>
        <p>Số lượng cảnh báo: {{ suricata_alerts|length }}</p>
        
        {% if chart_path %}
        <div class="chart">
            <img src="{{ chart_path }}" alt="Tóm tắt cảnh báo Suricata">
        </div>
        {% endif %}
        
        <h3>Cảnh báo Suricata</h3>
        <table>
            <tr>
                <th>STT</th>
                <th>Thời gian</th>
                <th>Nguồn</th>
                <th>Đích</th>
                <th>Giao thức</th>
                <th>Signature</th>
                <th>Mức độ</th>
            </tr>
            {% for alert in suricata_alerts %}
            <tr>
                <td>{{ loop.index }}</td>
                <td>{{ alert.timestamp }}</td>
                <td>{{ alert.src_ip }}{% if alert.src_port %}:{{ alert.src_port }}{% endif %}</td>
                <td>{{ alert.dest_ip }}{% if alert.dest_port %}:{{ alert.dest_port }}{% endif %}</td>
                <td>{{ alert.proto }}</td>
                <td>{{ alert.alert.signature }}</td>
                <td class="{% if alert.alert.severity >= 5 %}severity-high{% elif alert.alert.severity >= 3 %}severity-medium{% else %}severity-low{% endif %}">
                    {{ alert.alert.severity }}
                </td>
            </tr>
            {% endfor %}
        </table>
        {% else %}
        <p>Không có cảnh báo Suricata nào được phát hiện hoặc Suricata không được cài đặt.</p>
        {% endif %}
    </div>
    
    <footer>
        <p>Báo cáo được tạo tự động bởi công cụ phân tích bất thường mạng</p>
    </footer>
</body>
</html>
    """
    
    # Tạo báo cáo HTML
    try:
        template = jinja2.Template(template_str)
        report_html = template.render(**template_data)
        
        # Ghi ra file
        report_path = os.path.join(output_dir, "report.html")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_html)
        
        logger.info(f"Đã tạo báo cáo HTML tại: {report_path}")
        return report_path
    
    except Exception as e:
        logger.error(f"Lỗi khi tạo báo cáo HTML: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Công cụ tự động hóa phân tích bất thường mạng')
    parser.add_argument('-d', '--dir', default='./anomaly_reports', help='Thư mục chứa báo cáo (mặc định: ./anomaly_reports)')
    parser.add_argument('-o', '--output', default='./reports', help='Thư mục lưu kết quả phân tích (mặc định: ./reports)')
    parser.add_argument('--date', help='Chỉ xử lý báo cáo của ngày cụ thể (định dạng: YYYY-MM-DD)')
    parser.add_argument('--flow-id', help='Chỉ xử lý báo cáo của flow ID cụ thể')
    parser.add_argument('--no-recursive', action='store_true', help='Không tìm kiếm đệ quy trong thư mục')
    parser.add_argument('--no-charts', action='store_true', help='Không tạo biểu đồ')
    
    # Các tham số Suricata
    parser.add_argument('-s', '--suricata', default='suricata', help='Đường dẫn đến Suricata binary (mặc định: suricata)')
    parser.add_argument('--suricata-config', help='File cấu hình Suricata')
    parser.add_argument('--suricata-rules', default='/var/lib/suricata/rules', help='Thư mục chứa rules Suricata (mặc định: /var/lib/suricata/rules)')
    
    # Các tham số tích hợp
    parser.add_argument('--json2pcap', default='./json2pcap.py', help='Đường dẫn đến công cụ json2pcap.py (mặc định: ./json2pcap.py)')
    parser.add_argument('--suricata-analyzer', default='./suricata_analyzer.py', help='Đường dẫn đến công cụ suricata_analyzer.py (mặc định: ./suricata_analyzer.py)')
    
    # Các tùy chọn bỏ qua bước
    parser.add_argument('--skip-suricata', action='store_true', help='Bỏ qua bước phân tích Suricata')
    
    args = parser.parse_args()
    
    try:
        os.makedirs(args.output, exist_ok=True)
    except Exception as e:
        logger.error(f"Lỗi khi tạo thư mục đầu ra: {e}")
        return 1
    
    # Bước 1: Chuyển đổi JSON sang PCAP
    logger.info("[+] Chuyển đổi báo cáo JSON sang PCAP...")
    pcap_output = os.path.join(args.output, "reconstructed.pcap")
    pcap_file = run_json2pcap(
        args.json2pcap, 
        args.dir, 
        pcap_output, 
        args.date, 
        args.flow_id, 
        not args.no_recursive
    )
    
    if not pcap_file:
        logger.error("[!] Không thể chuyển đổi báo cáo JSON sang PCAP.")
        return 1
    
    # Bước 2: Phân tích PCAP với Suricata (nếu không bỏ qua)
    suricata_alerts = []
    suricata_chart = None
    
    if not args.skip_suricata:
        logger.info("[+] Phân tích PCAP với Suricata...")
        suricata_output_dir = os.path.join(args.output, "suricata")
        eve_json = run_suricata_analyzer(
            args.suricata_analyzer,
            pcap_file,
            suricata_output_dir,
            args.suricata,
            args.suricata_config,
            args.suricata_rules
        )
        
        if eve_json:
            suricata_alerts = parse_eve_json(eve_json)
            logger.info(f"[+] Đã phát hiện {len(suricata_alerts)} cảnh báo Suricata.")
            
            # Tạo biểu đồ tóm tắt Suricata
            if suricata_alerts and not args.no_charts:
                suricata_chart = create_suricata_summary_chart(
                    suricata_alerts, 
                    output_file=os.path.join(args.output, "suricata_summary.png")
                )
    
    # Bước 3: Tạo báo cáo HTML
    logger.info("[+] Tạo báo cáo HTML...")
    report_file = create_html_report(
        pcap_file=pcap_file,
        suricata_alerts=suricata_alerts,
        suricata_chart=suricata_chart,
        output_dir=args.output
    )
    
    if report_file:
        logger.info(f"[+] Báo cáo HTML đã được tạo: {report_file}")
        return 0
    else:
        logger.error("[!] Không thể tạo báo cáo HTML")
        return 1

if __name__ == "__main__":
    sys.exit(main())

def _process_report(self, report_json, address):
    try:
        report = json.loads(report_json)
        ...
    except json.JSONDecodeError:
        logger.warning(f"Dữ liệu không hợp lệ từ {address[0]}: {report_json}")
    except Exception as e:
        logger.error(f"Lỗi khi xử lý báo cáo từ {address[0]}: {e}")