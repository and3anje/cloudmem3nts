#!/usr/bin/env python3
import os
import shutil
import requests
import json
import datetime

# ── Configuration ──
SERVERS = [
    {
        "name": "web-server-01",
        "ip": "10.0.0.1",
        "check_url": "http://wttr.in/Nairobi?format=j1",
        "disk_threshold": 5,
        "memory_threshold": 80
    },
    {
        "name": "db-server-01", 
        "ip": "10.0.0.2",
        "check_url": "http://wttr.in/London?format=j1",
        "disk_threshold": 70,
        "memory_threshold": 75
    },
    {
        "name": "api-server-01",
        "ip": "10.0.0.3",
        "check_url": "http://wttr.in/Chuka?format=j1",
        "disk_threshold": 80,
        "memory_threshold": 80
    }
]

LOG_FILE = "monitoring.log"
REPORT_FILE = "monitoring_report.json"
alerts = []

# ── Logging ──
def log(level, server_name, message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    entry = f"[{timestamp}] [{level}] [{server_name}] {message}"
    
    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")
    
    print(entry)
    
    if level == "ALERT":
        alerts.append({
            "timestamp": timestamp,
            "server": server_name,
            "message": message
        })

# ── Individual Checks ──
def check_disk(server_name, threshold):
    total, used, free = shutil.disk_usage('/')
    percent = (used / total) * 100
    free_gb = free / (1024**3)
    
    if percent > threshold:
        log("ALERT", server_name, f"Disk usage critical: {percent:.1f}% (threshold: {threshold}%)")
        return False
    else:
        log("OK", server_name, f"Disk usage normal: {percent:.1f}% — {free_gb:.1f}GB free")
        return True

def check_memory(server_name, threshold):
    try:
        with open('/proc/meminfo', 'r') as f:
            meminfo = f.read()
        
        lines = meminfo.split('\n')
        mem_total = int([x for x in lines if 'MemTotal' in x][0].split()[1])
        mem_available = int([x for x in lines if 'MemAvailable' in x][0].split()[1])
        
        used_percent = ((mem_total - mem_available) / mem_total) * 100
        available_gb = mem_available / (1024**2)
        
        if used_percent > threshold:
            log("ALERT", server_name, f"Memory usage critical: {used_percent:.1f}% (threshold: {threshold}%)")
            return False
        else:
            log("OK", server_name, f"Memory usage normal: {used_percent:.1f}% — {available_gb:.1f}GB available")
            return True
            
    except Exception as e:
        log("ALERT", server_name, f"Memory check failed: {e}")
        return False

def check_connectivity(server_name, url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            log("OK", server_name, f"Connectivity check passed — status {response.status_code}")
            return True
        else:
            log("ALERT", server_name, f"Connectivity check failed — status {response.status_code}")
            return False
    except requests.exceptions.Timeout:
        log("ALERT", server_name, "Connectivity check timed out")
        return False
    except requests.exceptions.ConnectionError:
        log("ALERT", server_name, "Connection error — server unreachable")
        return False

# ── Main Monitor ──
def check_server(server):
    name = server['name']
    log("INFO", name, "Starting health check")
    
    disk_ok = check_disk(name, server['disk_threshold'])
    memory_ok = check_memory(name, server['memory_threshold'])
    connectivity_ok = check_connectivity(name, server['check_url'])
    
    overall = disk_ok and memory_ok and connectivity_ok
    status = "HEALTHY" if overall else "DEGRADED"
    
    log("INFO", name, f"Health check complete — {status}")
    return {
        "server": name,
        "ip": server['ip'],
        "status": status,
        "checks": {
            "disk": "OK" if disk_ok else "ALERT",
            "memory": "OK" if memory_ok else "ALERT",
            "connectivity": "OK" if connectivity_ok else "ALERT"
        }
    }

def run_monitoring():
    log("INFO", "SYSTEM", "=== Monitoring cycle started ===")
    results = []
    
    for server in SERVERS:
        result = check_server(server)
        results.append(result)
        print()
    
    return results

def generate_report(results):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    healthy = len([r for r in results if r['status'] == 'HEALTHY'])
    degraded = len([r for r in results if r['status'] == 'DEGRADED'])
    
    report = {
        "generated_at": timestamp,
        "summary": {
            "total_servers": len(results),
            "healthy": healthy,
            "degraded": degraded,
            "total_alerts": len(alerts)
        },
        "servers": results,
        "alerts": alerts
    }
    
    with open(REPORT_FILE, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n{'='*50}")
    print(f"MONITORING SUMMARY")
    print(f"{'='*50}")
    print(f"Total servers: {len(results)}")
    print(f"Healthy: {healthy}")
    print(f"Degraded: {degraded}")
    print(f"Total alerts: {len(alerts)}")
    print(f"Report saved: {REPORT_FILE}")
    print(f"{'='*50}")

# Main execution
results = run_monitoring()
generate_report(results)