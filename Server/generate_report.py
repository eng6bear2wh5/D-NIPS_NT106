import os
import sys
import json
from datetime import datetime
import jinja2

def parse_eve_json(eve_json):
    alerts = []
    with open(eve_json, 'r') as f:
        for line in f:
            try:
                event = json.loads(line.strip())
                if event.get("event_type") == "alert":
                    alerts.append(event)
            except Exception:
                continue
    return alerts

def create_html_report(eve_json, output_html, chart_path=None):
    alerts = parse_eve_json(eve_json)
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    template_str = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo cáo Suricata</title>
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
        <h1>Báo cáo Suricata</h1>
        <p>Ngày tạo báo cáo: {{ date }}</p>
    </div>
    <div class="section">
        <h2>Phân tích Suricata</h2>
        {% if alerts %}
        <h3>Tổng quan</h3>
        <p>Số lượng cảnh báo: {{ alerts|length }}</p>
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
            {% for alert in alerts %}
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
    template = jinja2.Template(template_str)
    html = template.render(date=today, alerts=alerts, chart_path=chart_path)
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Đã tạo báo cáo HTML: {output_html}")

if __name__ == "__main__":
    if len(sys.argv) not in [3, 4]:
        print("Usage: python3 generate_report.py <eve.json> <output.html> [chart.png]")
        sys.exit(1)
    eve_json = sys.argv[1]
    output_html = sys.argv[2]
    chart_path = sys.argv[3] if len(sys.argv) == 4 else None
    create_html_report(eve_json, output_html, chart_path)