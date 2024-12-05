<h1 align="center">
  Xray-Load-Balancer
</h1>

<h2 align="center">
Create a Load Balancer Xray Config.
</h2>

# Usage
🟢 YouTube Tutorial [here](https://www.youtube.com/watch?v=Cj4nmikSSpA)

🟢 Linux:

```bash
bash <(curl -s https://raw.githubusercontent.com/Surfboardv2ray/Xray-Load-Balancer/main/ubuntu.sh)
```

🟢 Android Termux:

```bash
bash <(curl -s https://raw.githubusercontent.com/Surfboardv2ray/Xray-Load-Balancer/main/termux.sh)
```

> [!CAUTION]
> Installation includes git, python, package updates and python requirements. Please note that, specially for running Android Termux locally, it will bypass y/n prompt and default to install without confirmation, resulting in charging you extra for downloaded packages; if not priorly installed.

<br>

🟡 Python Anywhere

Deploying on [pythonanywhere](https://www.pythonanywhere.com/), run the Linux command on a bash console. Edit your webapp `wsgi.py` file as following (replace `your_username` with your own):
```python
import sys
import os
project_home = '/home/your_username/Xray-Load-Balancer'
if project_home not in sys.path:
    sys.path.insert(0, project_home)
os.chdir(project_home)
from server import app as application
```


![0](https://raw.githubusercontent.com/Surfboardv2ray/v2ray-refiner/90c9fe1c9b4c3836d09e925af2398681343c5ff1/assets/redline.gif)

## Supported Protocols

🟡 Below is the list of currently supported protocols for creating a Load Balancer Xray config:

- VLESS+GRPC
- VLESS+GRPC+TLS
- VLESS+TCP
- VLESS+TCP+HTTP
- VLESS+TCP+TLS
- VLESS+TCP+TLS+HTTP
- VLESS+TCP+REALITY
- VLESS+GRPC+REALITY
- VLESS+WS
- VLESS+WS+TLS
- VLESS+WS+HTTP
- VLESS+WS+HTTP+TLS
- VMESS+GRPC
- VMESS+GRPC+TLS
- VMESS+TCP
- VMESS+TCP+HTTP
- VMESS+TCP+TLS
- VMESS+TCP+TLS+HTTP
- VMESS+WS
- VMESS+WS+TLS
- VMESS+WS+HTTP
- VMESS+WS+HTTP+TLS
- TROJAN+TCP
- TROJAN+TCP+HTTP
- TROJAN+TCP+TLS
- TROJAN+TCP+TLS+HTTP
- TROJAN+TCP+REALITY
- TROJAN+GRPC+REALITY
- TROJAN+GRPC+TLS
- TROJAN+WS
- TROJAN+WS+TLS
- TROJAN+WS+HTTP
- TROJAN+WS+HTTP+TLS

![0](https://raw.githubusercontent.com/Surfboardv2ray/v2ray-refiner/90c9fe1c9b4c3836d09e925af2398681343c5ff1/assets/redline.gif)

# Acknowledgements
🟡 v2ray to JSON converter copyrights to [Am-Delta](https://github.com/Am-Delta/v2ray-to-json). They're using Unlicense license for their script.

🟡 Base JSON derived from [Xray Proxy Grabber](https://github.com/MrMohebi/xray-proxy-grabber-telegram). They're using MIT License.
