# rules_engine.py
import time
import os
import re
from collections import defaultdict

traffic_history = defaultdict(list)
alert_cooldown = {}

class DDoSRule:
    def __init__(self, sid, threshold, window, msg, cooldown=60):
        self.sid = sid
        self.threshold = threshold
        self.window = window
        self.msg = msg
        self.cooldown = cooldown

    def match(self, packet):
        ip = packet.get("src_ip")
        now = time.time()

        traffic_history[ip].append(now)
        traffic_history[ip] = [t for t in traffic_history[ip] if now - t <= self.window]

        last_alert = alert_cooldown.get(ip, 0)
        if len(traffic_history[ip]) > self.threshold and now - last_alert > self.cooldown:
            alert_cooldown[ip] = now
            return True

        return False

    def get_alert(self, packet):
        return {
            "msg": self.msg,
            "sid": self.sid,
            "src_ip": packet.get("src_ip"),
            "agent_id": packet.get("agent_id")
        }

rules = []

def load_rules_from_file(filename):
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            match = re.match(r'ddos .* \(msg:"(.*?)"; threshold:(\d+),(\d+); sid:(\d+);?\)', line)
            if match:
                msg, threshold, window, sid = match.groups()
                rule = DDoSRule(
                    sid=int(sid),
                    threshold=int(threshold),
                    window=int(window),
                    msg=msg
                )
                rules.append(rule)

# Load all .rules files
def load_all_rules():
    rule_dir = "./rules"
    for filename in os.listdir(rule_dir):
        if filename.endswith(".rules"):
            load_rules_from_file(os.path.join(rule_dir, filename))

load_all_rules()

def check_rules(packet):
    alerts = []
    for rule in rules:
        if rule.match(packet):
            alerts.append(rule.get_alert(packet))
    return alerts
