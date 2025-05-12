from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

# In-memory store for packets.
packets_store = []
packet_id_counter = 1

@app.route('/api/add_packet', methods=['POST'])
def add_packet_route():
    global packet_id_counter
    try:
        # Expecting a list of packet data objects from the sender
        # Each object in the list is: {"packet_info": {}, "is_anomaly": int, "anomaly_score": float, "flow_score": float}
        list_of_packets_data = request.get_json()
        
        if not isinstance(list_of_packets_data, list):
            return jsonify({"error": "Invalid data format. Expected a list of packet objects."}), 400

        processed_ids = []
        for packet_data_item in list_of_packets_data:
            if not isinstance(packet_data_item, dict):
                print(f"Skipping non-dict item in batch: {packet_data_item}")
                continue

            packet_info = packet_data_item.get("packet_info")
            is_anomaly = packet_data_item.get("is_anomaly")
            anomaly_score = packet_data_item.get("anomaly_score")
            flow_score = packet_data_item.get("flow_score")

            # Basic validation for the structure of each item
            if not isinstance(packet_info, dict) or not isinstance(is_anomaly, int) or \
               not (isinstance(anomaly_score, (int, float))) or not (isinstance(flow_score, (int, float))):
                print(f"Skipping malformed packet data item: {packet_data_item}")
                continue

            # Extract data from packet_info
            packet_time = packet_info.get("timestamp", datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3])
            src_ip = packet_info.get("src_ip", "Unknown")
            dst_ip = packet_info.get("dst_ip", "Unknown")
            protocol = packet_info.get("protocol", "Unknown")
            src_port = str(packet_info.get("src_port", "N/A"))
            dst_port = str(packet_info.get("dst_port", "N/A"))
            app_proto = packet_info.get("app_proto", "")
            size = str(packet_info.get("size", "N/A"))
            details = packet_info.get("details", "")

            status_text = "Anomaly" if is_anomaly == -1 else "OK"

            # Order must match the table headers in table.py
            # Headers: "No.", "Time", "Src IP", "Dst IP", "Protocol", 
            #            "Src Port", "Dst Port", "App Proto", "Size", 
            #            "Status", "Anomaly Score", "Flow Score", "Details"
            formatted_packet_row = [
                str(packet_id_counter),
                packet_time,
                src_ip,
                dst_ip,
                protocol,
                src_port,
                dst_port,
                app_proto,
                size,
                status_text,
                f"{anomaly_score:.2f}" if isinstance(anomaly_score, float) else str(anomaly_score),
                f"{flow_score:.2f}" if isinstance(flow_score, float) else str(flow_score),
                details
            ]
            packets_store.append(formatted_packet_row)
            processed_ids.append(str(packet_id_counter))
            packet_id_counter += 1
        
        if not processed_ids:
             return jsonify({"message": "No valid packets processed from the batch."}), 200

        print(f"Dashboard API processed {len(processed_ids)} packets from batch.")
        return jsonify({"message": f"{len(processed_ids)} packets added successfully to Dashboard API", "packet_ids": processed_ids}), 201
    except Exception as e:
        print(f"Error in Dashboard API /api/add_packet: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/get_packets', methods=['GET'])
def get_packets_route():
    global packets_store
    packets_to_send = list(packets_store) 
    packets_store.clear() 
    return jsonify(packets_to_send), 200

if __name__ == '__main__':
    # To run this API:
    # 1. Navigate to the Dashboard directory: cd /home/rigil/PacketSniffer/D-NIPS_NT106/Dashboard
    # 2. Activate the virtual environment: source .venv/bin/activate
    # 3. Run the api: python dashboard_api.py
    # The API will run on http://localhost:5001
    app.run(host='0.0.0.0', port=5001, debug=True)
