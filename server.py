from flask import Flask, request, jsonify
import subprocess
import json
import copy  # Import copy module

app = Flask(__name__)

# Base configuration template
base_config_template = {
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
        "hosts": {"domain:googleapis.cn": "googleapis.com"},
        "servers": ["1.1.1.1"]
    },
    "inbounds": [
        {
            "listen": "127.0.0.1",
            "port": 10808,
            "protocol": "socks",
            "settings": {"auth": "noauth", "udp": True, "userLevel": 8},
            "sniffing": {"destOverride": ["http", "tls"], "enabled": True},
            "tag": "socks"
        },
        {
            "listen": "127.0.0.1",
            "port": 10809,
            "protocol": "http",
            "settings": {"userLevel": 8},
            "tag": "http"
        }
    ],
    "log": {"loglevel": "warning"},
    "outbounds": [
        {"protocol": "freedom", "tag": "direct-out"}
    ],
    "policy": {
        "levels": {
            "8": {"connIdle": 300, "downlinkOnly": 1, "handshake": 4, "uplinkOnly": 1}
        },
        "system": {"statsOutboundDownlink": True, "statsOutboundUplink": True}
    },
    "routing": {
        "balancers": [
            {
                "selector": [],
                "strategy": {"type": "leastLoad"},
                "tag": "public-proxies"
            }
        ],
        "domainMatcher": "hybrid",
        "domainStrategy": "IPIfNonMatch",
        "rules": [
            {
                "balancerTag": "public-proxies",
                "inboundTag": ["socks", "http"],
                "type": "field"
            }
        ]
    },
    "stats": {}
}

@app.route("/")
def home():
    return open("index.html").read()

@app.route("/convert", methods=["POST"])
def convert():
    # Create a fresh copy of base_config for this request
    base_config = copy.deepcopy(base_config_template)

    data = request.get_json()
    configs = data.get("config", "").strip().splitlines()

    processed_proxies = []
    proxy_count = 0

    for config in configs:
        try:
            # Run py on each configuration
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
