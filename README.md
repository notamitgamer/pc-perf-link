> [!WARNING]
> ## LOW ACTIVITY REPOSITORY
>
> This project is not abandoned, but it receives updates very infrequently. <br>
> ***Issues and Pull Requests may be submitted, but expect significant delays in reviews.***
---

# pc-perf-link

A real-time hardware monitoring system that bridges your PC telemetry to any external device. This project provides a low-latency, high-performance dashboard designed to turn any smartphone, tablet, or secondary computer into a dedicated system monitor.

## Features

- Live Telemetry: Real-time CPU, RAM, Network, and Disk I/O monitoring via WebSockets.
- App Tracking: View top memory-consuming applications directly from your remote device.
- Benchmarking Suite: Record sessions to calculate a custom optimization score.
- Universal Compatibility: Fully responsive UI optimized for all modern browsers and screen sizes.
- Lightweight Backend: Powered by FastAPI and psutil for minimal host PC overhead.

## Installation

1. Install the required Python dependencies:
   pip install fastapi uvicorn psutil

2. Ensure you have the following files in the same directory:
   - server_bridge.py
   - index.html
   - style.css
   - chart.js

## Usage

1. Start the server on your host PC:
   python server_bridge.py

2. Note the local IP address displayed in the console (e.g., 192.168.1.5).
3. Connect your secondary device (phone, tablet, or laptop) to the same local network.
4. Open the web browser on that device and navigate to:
   http://[YOUR_PC_IP]:8000

5. Enter the host PC's IP address in the setup screen to initialize the stream.

## Benchmarking Score

The dashboard features a "Record" mode to track system performance during specific tasks.
Formula: (Time in seconds * 50) + (Peak CPU %) + (RAM Delta GB * 200)
A lower score indicates better optimization.

## Security and Support

Immediate security concerns: amitdutta4255@gmail.com
Normal bugs or suggestions: mail@amit.is-a.dev

## License

This project is open-source. Please refer to the [LICENSE](LICENSE) file for details.
