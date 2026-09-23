#!/usr/bin/env python3
"""
AEGIS-MONAD Real Hardware Daemon Client (Linux Distros)
Collects physical system telemetry (CPU, GPU, Memory Bandwidth, Power) and streams to SOC Dashboard.
"""

import time
import json
import socket
import urllib.request
import os
import sys

# Central Dashboard Endpoint
DASHBOARD_URL = os.getenv("AEGIS_DASHBOARD_URL", "http://127.0.0.1:7860/api/hardware_telemetry")
HW_KEY = "HW_KEY_0x889_BSU_DAS_2026_EDR"

def get_sys_metrics():
    """Extracts live telemetry using Linux native /proc and /sys filesystem statistics."""
    hostname = socket.gethostname()
    
    # 1. CPU Load
    try:
        load1, load5, _ = os.getloadavg()
    except Exception:
        load1, load5 = 0.0, 0.0

    # 2. System Memory (from /proc/meminfo)
    mem_total, mem_free = 0, 0
    if os.path.exists("/proc/meminfo"):
        with open("/proc/meminfo", "r") as f:
            for line in f:
                if "MemTotal:" in line:
                    mem_total = int(line.split()[1]) // 1024  # MB
                elif "MemAvailable:" in line:
                    mem_free = int(line.split()[1]) // 1024   # MB
    mem_used = mem_total - mem_free

    # 3. Network Throughput (from /proc/net/dev)
    rx_bytes, tx_bytes = 0, 0
    if os.path.exists("/proc/net/dev"):
        with open("/proc/net/dev", "r") as f:
            for line in f.readlines()[2:]:
                parts = line.split()
                if len(parts) >= 10 and not parts[0].startswith("lo:"):
                    rx_bytes += int(parts[1])
                    tx_bytes += int(parts[9])

    return {
        "hostname": hostname,
        "hardware_key": HW_KEY,
        "os_distro": sys.platform,
        "timestamp": time.time(),
        "cpu_load_1min": load1,
        "cpu_load_5min": load5,
        "mem_total_mb": mem_total,
        "mem_used_mb": mem_used,
        "net_rx_kb": round(rx_bytes / 1024.0, 2),
        "net_tx_kb": round(tx_bytes / 1024.0, 2),
        "status": "ONLINE_ACTIVE"
    }

def main():
    print(f"[*] Starting AEGIS Real Hardware Client on {socket.gethostname()}...")
    print(f"[*] Targeting SOC Dashboard: {DASHBOARD_URL}")
    
    while True:
        payload = get_sys_metrics()
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(DASHBOARD_URL, data=data, headers={"Content-Type": "application/json"})
        
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    print(f"[{time.strftime('%H:%M:%S')}] Telemetry synced -> CPU Load: {payload['cpu_load_1min']} | RAM: {payload['mem_used_mb']}/{payload['mem_total_mb']} MB")
        except Exception as e:
            print(f"[!] Sync error: {e}")
            
        time.sleep(3)

if __name__ == "__main__":
    main()
