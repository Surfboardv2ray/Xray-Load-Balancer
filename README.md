<h1 align="center">
  Xray-Load-Balancer
</h1>

<h2 align="center">
Create a Load Balancer Xray Config.
</h2>

# Usage
🟢 Linux:

```bash
apt update
apt ugprade -y
apt install git -y
apt install python3-pip -y
python3 -m pip install --upgrade pip -y
git clone https://github.com/Surfboardv2ray/Xray-Load-Balancer.git
cd Xray-Load-Balancer
pip3 install -r requirements.txt
python3 server.py

```

🟢 Android Termux:

```bash
git clone https://github.com/Surfboardv2ray/Xray-Load-Balancer.git
cd Xray-Load-Balancer
pip install -r requirements.txt
python server.py

```

![0](https://raw.githubusercontent.com/Surfboardv2ray/v2ray-refiner/90c9fe1c9b4c3836d09e925af2398681343c5ff1/assets/redline.gif)

## Supported Porotocls

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
