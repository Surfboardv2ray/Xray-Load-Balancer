from flask import Flask, request, jsonify
import subprocess
import json
import copy

app = Flask(__name__)

# Base
base_config_template = {
  "remarks": "Xray-Load-Balancer (Surfboardv2ray)",
  "log": {
    "access": "",
    "error": "",
    "loglevel": "warning"
  },
  "inbounds": [
    {
      "tag": "socks",
      "port": 10808,
      "listen": "0.0.0.0",
      "protocol": "socks",
      "sniffing": {
        "enabled": True,
        "destOverride": [
          "http",
          "tls"
        ],
        "routeOnly": False
      },
      "settings": {
        "auth": "noauth",
        "udp": True,
        "allowTransparent": False
      }
    },
    {
      "tag": "http",
      "port": 10809,
      "listen": "0.0.0.0",
      "protocol": "http",
      "sniffing": {
        "enabled": True,
        "destOverride": [
          "http",
          "tls"
        ],
        "routeOnly": False
      },
      "settings": {
        "auth": "noauth",
        "udp": True,
        "allowTransparent": False
      }
    },
    {
      "tag": "api",
      "port": 10813,
      "listen": "127.0.0.1",
      "protocol": "dokodemo-door",
      "settings": {
        "udp": False,
        "address": "127.0.0.1",
        "allowTransparent": False
      }
    }
  ],
  "outbounds": [
    {
      "protocol": "freedom",
      "tag": "direct-out"
    }
  ],
  "stats": {},
  "api": {
    "tag": "api",
    "services": [
      "StatsService"
    ]
  },
  "policy": {
    "system": {
      "statsOutboundUplink": True,
      "statsOutboundDownlink": True
    }
  },
  "burstObservatory": {
    "pingConfig": {
      "connectivity": "http://connectivitycheck.platform.hicloud.com/generate_204",
      "destination": "http://www.google.com/gen_204",
      "interval": "15m",
      "sampling": 2,
      "timeout": "3s"
    },
    "subjectSelector": []
  },
  "dns": {
    "hosts": {
      "domain:googleapis.cn": "googleapis.com"
    },
    "servers": [
      "1.1.1.1"
    ]
  },
  "routing": {
    "balancers": [
      {
        "selector": [],
        "strategy": {
          "type": "leastLoad"
        },
        "tag": "xray-load-balancer"
      }
    ],
    "domainMatcher": "hybrid",
    "domainStrategy": "IPIfNonMatch",
    "rules": [
      {
        "balancerTag": "xray-load-balancer",
        "inboundTag": [
          "socks",
          "http"
        ],
        "type": "field"
      }
    ]
  }
}


@app.route("/")
def home():
    return open("index.html").read()

@app.route("/convert", methods=["POST"])
def convert():

    base_config = copy.deepcopy(base_config_template)

    data = request.get_json()
    configs = data.get("config", "").strip().splitlines()

    processed_proxies = []
    proxy_count = 0

    for config in configs:
        try:
            result = subprocess.run(
                ["python3", "v2tj.py", config],
                text=True,
                capture_output=True
            )

            # Skip configs that fail to convert
            if result.returncode != 0:
                continue

            # Parse the converted JSON
            converted_config = json.loads(result.stdout)

            # Extract outbounds with the "proxy" tag
            proxy_outbound = next(
                (outbound for outbound in converted_config.get("outbounds", [])
                 if outbound.get("tag") == "proxy"),
                None
            )

            # Skip if no "proxy" outbound is found
            if not proxy_outbound:
                continue

            # Rename the tag and increment the counter
            proxy_count += 1
            new_tag = f"proxy-{proxy_count}"
            proxy_outbound["tag"] = new_tag

            # Add to processed proxies and selectors
            processed_proxies.append(proxy_outbound)
            base_config["burstObservatory"]["subjectSelector"].append(new_tag)
            base_config["routing"]["balancers"][0]["selector"].append(new_tag)

        except (subprocess.CalledProcessError, json.JSONDecodeError, KeyError):
            # Skip this config if an error occurs
            continue

    # Return an error if no proxies were successfully processed
    if not processed_proxies:
        return jsonify({"error": "No valid configurations could be processed."}), 400

    # Add all processed proxies to the base configuration's outbounds
    base_config["outbounds"] = processed_proxies + base_config["outbounds"]

    return jsonify({"result": json.dumps(base_config, indent=2)})



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
