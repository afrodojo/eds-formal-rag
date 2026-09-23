#!/usr/bin/env python3
"""
AEGIS-MONAD Multi-User & Physical Peripheral Hardware Daemon Client
Supports real Linux devices, custom user node registration, display monitor detection,
and active network interface telemetry.
"""

import time
import json
import socket
import urllib.request
import os
import sys
import glob

DASHBOARD_URL = os.getenv("AEGIS_DASHBOARD_URL", "http://127.0.0.1:7860/api/hardware_telemetry")
HW_KEY = os.getenv("AEGIS_HW_KEY", "HW_KEY_0x889_BSU_DAS_2026_EDR")
NODE_OWNER = os.getenv("AEGIS_NODE_OWNER", os.getenv("USER", "analyst_node"))

def get_connected_monitors():
    """Detects physically connected monitors/displays via Linux /sys/class/drm."""
    monitors = []
    try:
        status_files = glob.glob("/sys/class/drm/*/status")
        for f in status_files:
            with open(f, "r") as file:
                if file.read().strip() == "connected":
                    output_name = f.split("/sys/class/drm/card0-")[-1].replace("/status", "")
                    monitors.append(output_name)
    except Exception:
        monitors = ["Default_Display"]
    return monitors if monitors else ["Headless / No Monitor"]

def get_network_interfaces():
    """Enumerates physical network adapters and active IP configurations."""
    interfaces = {}
    if os.path.exists("/proc/net/dev"):
        with open("/proc/net/dev", "r") as f:
            for line in f.readlines()[2:]:
                parts = line.split()
                if len(parts) >= 10 and not parts[0].startswith("lo:"):
                    iface = parts[0].strip(":")
                    rx_bytes = int(parts[1]) // 1024
                    tx_bytes = int(parts[9]) // 1024
                    interfaces[iface] = {"rx_kb": rx_bytes, "tx_kb": tx_bytes}
    return interfaces

def get_sys_metrics():
    hostname = socket.gethostname()
    try:
        load1, load5, _ = os.getloadavg()
    except Exception:
        load1, load5 = 0.0, 0.0

    mem_total, mem_free = 0, 0
    if os.path.exists("/proc/meminfo"):
        with open("/proc/meminfo", "r") as f:
            for line in f:
                if "MemTotal:" in line:
                    mem_total = int(line.split()[1]) // 1024
                elif "MemAvailable:" in line:
                    mem_free = int(line.split()[1]) // 1024

    return {
        "hostname": hostname,
        "owner": NODE_OWNER,
        "hardware_key": HW_KEY,
        "os_distro": sys.platform,
        "timestamp": time.time(),
        "cpu_load_1min": load1,
        "cpu_load_5min": load5,
        "mem_total_mb": mem_total,
        "mem_used_mb": mem_total - mem_free,
        "connected_monitors": get_connected_monitors(),
        "network_adapters": get_network_interfaces(),
        "status": "ONLINE_ACTIVE"
    }

def main():
    print(f"[*] Starting AEGIS Client for User/Owner: '{NODE_OWNER}' on Host: '{socket.gethostname()}'")
    print(f"[*] Target SIEM Dashboard Endpoint: {DASHBOARD_URL}")
    
    while True:
        payload = get_sys_metrics()
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(DASHBOARD_URL, data=data, headers={"Content-Type": "application/json"})
        
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    print(f"[{time.strftime('%H:%M:%S')}] Telemetry Synced -> Displays: {payload['connected_monitors']} | RAM: {payload['mem_used_mb']}/{payload['mem_total_mb']} MB")
        except Exception as e:
            print(f"[!] Sync error (retrying in 5s): {e}")
            
        time.sleep(5)

if __name__ == "__main__":
    main()
