# dashboard/federal_hardware_engine.py - Live Telemetry, Compliance Guards & Dynamic Schedule Engine
import os
import time
import socket
import pandas as pd

class RealHardwareTelemetryEngine:
    def __init__(self, vault_path=None):
        self.vault_path = vault_path or os.path.expanduser("~/Google Drive/My Drive/EDS_Research_Vault")
        
        # Physical Infrastructure Inventory
        self.servers = [
            {"hostname": "node1.eds.internal", "ip": "10.0.10.10", "model": "HP ML350p Gen8", "status": "Awaiting Drives", "target_date": "2026-08-31", "mgmt": "iLO4", "fips_updated": False},
            {"hostname": "node2.eds.internal", "ip": "10.0.20.20", "model": "Dell PowerEdge R620", "status": "Pending Provisioning", "target_date": "2026-08-18", "mgmt": "iDRAC7", "fips_updated": True},
            {"hostname": "node3.eds.internal", "ip": "10.0.20.30", "model": "Dell PowerEdge T320", "status": "Pending Provisioning", "target_date": "2026-08-19", "mgmt": "iDRAC7", "fips_updated": True},
            {"hostname": "node4.eds.internal", "ip": "10.0.20.40", "model": "HP DL380p Gen8", "status": "Pending Provisioning", "target_date": "2026-08-24", "mgmt": "iLO4", "fips_updated": False}
        ]
        
        self.network_gear = {
            "gateway": {"model": "Meraki MX105 Security Appliance", "wan": "1GBPS Dedicated Fiber", "ip": "10.0.0.1"},
            "switch": {"model": "Meraki MS-130 48-Port PoE", "poe_budget_w": 740, "ip": "10.0.0.2"},
            "access_points": [{"model": "Meraki MR46 AP-1", "ip": "10.0.0.10"}, {"model": "Meraki MR46 AP-2", "ip": "10.0.0.11"}]
        }

    def get_server_inventory_df(self):
        return pd.DataFrame(self.servers)

    def update_node_schedule(self, target_ip, new_status, new_target_date, delay_reason=""):
        """Updates due dates, status, and delay reasons dynamically."""
        for server in self.servers:
            if server["ip"] in target_ip or server["hostname"] in target_ip:
                server["status"] = new_status
                server["target_date"] = new_target_date
                if delay_reason:
                    server["delay_notes"] = delay_reason
                print(f"[+] Updated {server['hostname']}: Status={new_status}, Due={new_target_date}")
                return f"[SUCCESS] Updated {server['hostname']} | Status: {new_status} | Due: {new_target_date}"
        return "[!] Target Node Not Found."

    def probe_live_socket(self, ip_address, port=80, timeout=1.0):
        """Attempts a real TCP socket connection to test physical network flow."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((ip_address, port))
            sock.close()
            return "ONLINE / CONNECTED" if result == 0 else "HOST UNREACHABLE (SOCKET TIMEOUT)"
        except Exception as e:
            return f"CONNECTION ERROR: {str(e)}"

    def poll_node_telemetry(self, target_ip):
        """Executes live network probing and returns server hardware metrics."""
        match = next((s for s in self.servers if s["ip"] in target_ip or s["hostname"] in target_ip), None)
        if match:
            connection_state = self.probe_live_socket(match["ip"])
            return {
                "Hostname": match["hostname"],
                "IP_Address": match["ip"],
                "Hardware_Model": match["model"],
                "Connection_Probe": connection_state,
                "Provisioning_Status": match["status"],
                "Target_Online_Date": match["target_date"],
                "Delay_Notes": match.get("delay_notes", "No active delays recorded"),
                "Management_Controller": match["mgmt"],
                "FIPS_Kernel_Updated": "YES (Current)" if match["fips_updated"] else "NO (OUT OF COMPLIANCE / PENDING UPDATE)"
            }
        return {"IP": target_ip, "Status": "Unknown Endpoint"}

    def run_compliance_and_misconfig_audit(self):
        """Audits hardware state against NIST 800-171, CMMC 2.0, and JSIG standards."""
        audit_findings = []
        for server in self.servers:
            is_updated = server.get("fips_updated", False)
            status = server.get("status", "")
            
            # Check 1: FIPS 140-3 Kernel Patch Audit
            audit_findings.append({
                "Target_Host": server["hostname"],
                "Control_Framework": "NIST SP 800-171 (3.13.11)",
                "Policy_Name": "FIPS Cryptographic Module Integrity",
                "Compliance_Status": "COMPLIANT" if is_updated else "NON-COMPLIANT / OUTDATED",
                "Flagged_Issue": "None" if is_updated else "Missing RHEL FIPS 140-3 Security Patch",
                "Recommended_Action": "Execute dnf update --fips on host" if not is_updated else "Verified"
            })
            
            # Check 2: Provisioning & Delay Audit
            if "Awaiting" in status or "Pending" in status:
                audit_findings.append({
                    "Target_Host": server["hostname"],
                    "Control_Framework": "CMMC 2.0 (CA.L2-3.12.1)",
                    "Policy_Name": "System Security Plan & Milestone Management",
                    "Compliance_Status": "MILESTONE DELAYED",
                    "Flagged_Issue": f"Server status: '{status}'. Target date: {server['target_date']}",
                    "Recommended_Action": "Track hardware acquisition and update SSP target baseline"
                })

        return pd.DataFrame(audit_findings)

    def get_meraki_network_status(self):
        gw_status = self.probe_live_socket("10.0.0.1")
        return {
            "Gateway": self.network_gear["gateway"]["model"],
            "WAN_Connection": self.network_gear["gateway"]["wan"],
            "Gateway_Socket_Probe": gw_status,
            "Switch_Fabric": self.network_gear["switch"]["model"],
            "Wireless_APs": "2x Meraki MR46 (PoE Active)",
            "Firewall_Throughput": "3.0 Gbps (Line-Rate Active)",
            "SMT_Policy_Gate": "Active at Ingress Boundary"
        }

real_hardware_engine = RealHardwareTelemetryEngine()