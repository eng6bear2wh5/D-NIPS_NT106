#!/usr/bin/env python3
"""
PCAP Analysis Tool with Suricata and Results Display
"""

import os
import sys
import json
import argparse
import logging
import subprocess
import tempfile
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("SuricataAnalyzer")

class SuricataAnalyzer:
    def __init__(self, suricata_bin="suricata", config_file=None, rules_dir=None):
        self.suricata_bin = suricata_bin
        self.config_file = config_file
        self.rules_dir = rules_dir
        
        # Check if Suricata exists
        try:
            # Fixed: Use -V instead of --version
            version_cmd = [self.suricata_bin, "-V"]
            result = subprocess.run(version_cmd, capture_output=True, text=True)
            if result.returncode != 0:
                logger.error(f"Unable to run Suricata: {result.stderr}")
                raise RuntimeError("Suricata is not installed or cannot be accessed")
            
            logger.info(f"Found Suricata: {result.stdout.splitlines()[0].strip()}")
        
        except Exception as e:
            logger.error(f"Error checking Suricata: {e}")
            raise
    
    def analyze_pcap(self, pcap_file, output_dir=None):
        """Analyze PCAP file with Suricata"""
        # Create temporary directory if no output_dir provided
        if not output_dir:
            output_dir = tempfile.mkdtemp(prefix="suricata_")
            logger.info(f"Created temporary directory for results: {output_dir}")
        else:
            os.makedirs(output_dir, exist_ok=True)
        
        # Create Suricata command
        cmd = [self.suricata_bin, "-r", pcap_file, "-l", output_dir]
        
        # Add config file if provided
        if self.config_file:
            cmd.extend(["-c", self.config_file])
        
        # Specify rules directory if provided
        if self.rules_dir:
            cmd.extend(["--set", f"default-rule-path={self.rules_dir}"])
        
        # Enable EVE JSON mode
        cmd.extend(["--set", "outputs.1.eve-log.enabled=yes"])
        
        logger.info(f"Running Suricata with command: {' '.join(cmd)}")
        
        # Run Suricata
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"Suricata failed with return code {result.returncode}: {result.stderr}")
                return None
            
            logger.info("Suricata completed analysis")
            
            # Path to eve.json
            eve_json = os.path.join(output_dir, "eve.json")
            
            if not os.path.exists(eve_json):
                logger.error(f"Results file not found: {eve_json}")
                return None
            
            return eve_json
        
        except Exception as e:
            logger.error(f"Error running Suricata: {e}")
            return None

def parse_eve_json(eve_json):
    """Parse eve.json file and return alerts"""
    alerts = []
    
    try:
        # Read eve.json line by line (since it's not valid JSON as a whole)
        with open(eve_json, 'r') as f:
            for line in f:
                try:
                    event = json.loads(line.strip())
                    
                    # Only filter alert events
                    if event.get("event_type") == "alert":
                        alerts.append(event)
                
                except json.JSONDecodeError:
                    continue
        
        return alerts
    
    except Exception as e:
        logger.error(f"Error reading eve.json file: {e}")
        return []

def display_alerts(alerts):
    """Display Suricata alerts"""
    console = Console()
    
    if not alerts:
        console.print(Panel("[bold red]No alerts found from Suricata[/bold red]"))
        return
    
    # Display overview
    console.print(Panel(f"[bold]Found {len(alerts)} alerts from Suricata[/bold]"))
    
    # Create alerts table
    table = Table(title="Suricata Alerts", expand=True)
    table.add_column("No.", style="cyan", width=5)
    table.add_column("Timestamp", width=20)
    table.add_column("Src IP:Port", width=22)
    table.add_column("Dst IP:Port", width=22)
    table.add_column("Protocol", width=8)
    table.add_column("Signature ID", width=10)
    table.add_column("Signature", width=40)
    table.add_column("Severity", width=8)
    
    # Add data to table
    for i, alert in enumerate(alerts, 1):
        timestamp = alert.get("timestamp", "")
        
        src_ip = alert.get("src_ip", "")
        src_port = alert.get("src_port", "")
        src = f"{src_ip}:{src_port}" if src_port else src_ip
        
        dst_ip = alert.get("dest_ip", "")
        dst_port = alert.get("dest_port", "")
        dst = f"{dst_ip}:{dst_port}" if dst_port else dst_ip
        
        proto = alert.get("proto", "")
        
        alert_data = alert.get("alert", {})
        signature_id = str(alert_data.get("signature_id", ""))
        signature = alert_data.get("signature", "")
        severity = alert_data.get("severity", 0)
        
        # Color based on severity
        severity_style = "green"
        if severity >= 3:
            severity_style = "yellow"
        if severity >= 5:
            severity_style = "red"
        
        table.add_row(
            str(i),
            timestamp,
            src,
            dst,
            proto,
            signature_id,
            signature,
            f"[{severity_style}]{severity}[/{severity_style}]"
        )
    
    console.print(table)
    
    # Display common alert categories
    categories = {}
    for alert in alerts:
        category = alert.get("alert", {}).get("category", "Unknown")
        categories[category] = categories.get(category, 0) + 1
    
    console.print("\n[bold]Alert categories:[/bold]")
    for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        console.print(f"  - {category}: {count}")

def main():
    parser = argparse.ArgumentParser(description="Analyze PCAP files with Suricata and display results")
    parser.add_argument('pcap_file', help='PCAP file to analyze')
    parser.add_argument('-o', '--output', help='Output directory (default: temporary directory)')
    parser.add_argument('-s', '--suricata', default='suricata', help='Path to Suricata binary (default: suricata)')
    parser.add_argument('-c', '--config', help='Suricata configuration file')
    parser.add_argument('-r', '--rules', help='Directory containing Suricata rules')
    parser.add_argument('--summary', action='store_true', help='Only show alert summary')
    
    args = parser.parse_args()
    
    # Check PCAP file
    if not os.path.exists(args.pcap_file):
        logger.error(f"PCAP file does not exist: {args.pcap_file}")
        sys.exit(1)
    
    # Create analyzer
    try:
        analyzer = SuricataAnalyzer(
            suricata_bin=args.suricata,
            config_file=args.config,
            rules_dir=args.rules
        )
        
        # Analyze PCAP
        eve_json = analyzer.analyze_pcap(args.pcap_file, args.output)
        
        if not eve_json:
            logger.error("PCAP analysis failed")
            sys.exit(1)
        
        # Read and display alerts
        alerts = parse_eve_json(eve_json)
        display_alerts(alerts)
        
    except Exception as e:
        logger.error(f"Unhandled error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()