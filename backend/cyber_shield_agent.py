import psutil
import os
import signal

class CyberShieldAgent:
    def __init__(self):
        self.suspicious_ports = [4444, 1337, 31337] # Common malware ports
        self.whitelist_ips = ["127.0.0.1", "0.0.0.0"]

    def monitor_network(self):
        """Scans all active connections for suspicious activity."""
        connections = psutil.net_connections()
        threats = []
        for conn in connections:
            if conn.status == 'ESTABLISHED':
                remote_ip = conn.raddr.ip if conn.raddr else None
                remote_port = conn.raddr.port if conn.raddr else None
                
                if remote_port in self.suspicious_ports:
                    threats.append({
                        "pid": conn.pid,
                        "ip": remote_ip,
                        "port": remote_port,
                        "reason": "MALICIOUS_PORT_DETECTED"
                    })
        return threats

    def terminate_threat(self, pid: int):
        """Immediately kills the process associated with a threat."""
        try:
            process = psutil.Process(pid)
            name = process.name()
            # os.kill(pid, signal.SIGTERM) # Use SIGTERM first
            process.terminate()
            return f"Neural Guardian: Terminated suspicious process '{name}' (PID: {pid}). System status: SECURE."
        except Exception as e:
            return f"Neural Guardian Error: Failed to kill process {pid}. {e}"

cyber_shield = CyberShieldAgent()
