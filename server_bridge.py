import asyncio
import json
import time
import socket
import os
import psutil
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn

app = FastAPI(title="PC Monitor Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

last_net = psutil.net_io_counters()
last_disk = psutil.disk_io_counters()
last_time = time.time()

def get_top_apps(limit=6):
    """Groups running processes by name to approximate open user applications."""
    apps = {}
    for proc in psutil.process_iter(['name', 'memory_info']):
        try:
            name = proc.info['name']
            if name and name.lower().endswith('.exe'):
                name = name[:-4] # Clean up .exe extension
            mem = proc.info['memory_info'].rss / (1024 * 1024) # MB
            apps[name] = apps.get(name, 0) + mem
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # Filter out tiny background processes (< 50MB) to find true "Apps"
    significant_apps = {k: v for k, v in apps.items() if v > 50}
    
    # Sort by highest RAM usage
    sorted_apps = sorted(significant_apps.items(), key=lambda x: x[1], reverse=True)[:limit]
    
    return {
        "count": len(significant_apps),
        "top": [{"name": name, "mem_mb": round(mem, 1)} for name, mem in sorted_apps]
    }

def get_system_stats():
    global last_net, last_disk, last_time
    
    current_time = time.time()
    time_delta = current_time - last_time
    if time_delta == 0:
        time_delta = 1 

    cpu_percent = psutil.cpu_percent(interval=None)
    cpu_freq = psutil.cpu_freq()
    freq_current = round(cpu_freq.current / 1000, 2) if cpu_freq else 0.0

    ram = psutil.virtual_memory()
    ram_used_gb = round(ram.used / (1024**3), 2)
    ram_total_gb = round(ram.total / (1024**3), 2)
    
    current_net = psutil.net_io_counters()
    net_upload_speed = (current_net.bytes_sent - last_net.bytes_sent) / time_delta
    net_download_speed = (current_net.bytes_recv - last_net.bytes_recv) / time_delta
    
    current_disk = psutil.disk_io_counters()
    disk_write_speed = (current_disk.write_bytes - last_disk.write_bytes) / time_delta
    disk_read_speed = (current_disk.read_bytes - last_disk.read_bytes) / time_delta

    last_net = current_net
    last_disk = current_disk
    last_time = current_time

    uptime_seconds = int(current_time - psutil.boot_time())
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    return {
        "ip": get_local_ip(),
        "uptime": f"{hours}h {minutes}m",
        "cpu": {"percent": cpu_percent, "freq_ghz": freq_current},
        "ram": {"percent": ram.percent, "used_gb": ram_used_gb, "total_gb": ram_total_gb},
        "network": {"up_kbps": round(net_upload_speed / 1024, 1), "down_kbps": round(net_download_speed / 1024, 1)},
        "disk": {"read_kbps": round(disk_read_speed / 1024, 1), "write_kbps": round(disk_write_speed / 1024, 1)},
        "apps": get_top_apps() # <-- New App Data
    }

@app.get("/")
async def serve_ui():
    if os.path.exists("index.html"):
        return FileResponse("index.html")
    return {"error": "index.html not found!"}

@app.get("/style.css")
async def serve_css():
    if os.path.exists("style.css"):
        return FileResponse("style.css")
    return {"error": "style.css not found"}

@app.get("/chart.js")
async def serve_chart():
    if os.path.exists("chart.js"):
        return FileResponse("chart.js")
    return {"error": "chart.js not found"}

@app.websocket("/ws/stats")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    psutil.cpu_percent(interval=None)
    
    try:
        while True:
            stats = get_system_stats()
            await websocket.send_text(json.dumps(stats))
            await asyncio.sleep(1) 
    except Exception as e:
        print(f"Phone disconnected: {e}")

if __name__ == "__main__":
    print("Starting PC Monitor Server...")
    print(f"Mobile URL: http://{get_local_ip()}:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
