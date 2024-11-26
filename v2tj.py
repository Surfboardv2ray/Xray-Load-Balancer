import os
import json
import base64
from uuid import uuid4


def inbound_generator(host, port, socksport):
    inbound = {
        "inbounds": [
            {
                "tag": "socks",
                "port": socksport,
                "listen": host,
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
                "port": port,
                "listen": host,
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
            }
        ]
    }
    return inbound


def json_file_maker(data):
    print(json.dumps(data, indent=4))  # Pretty-printed JSON output
    return None  # No file is created or returned



def splitter(uri, target):
    if "&" in uri.split(target)[1]:
        spx = uri.split(target)[1].split("&")[0]
    elif "#" in uri.split(target)[1]:
        spx = uri.split(target)[1].split("#")[0]
    return spx


def convert_uri_reality_json(host, port, socksport, uri):

    protocol = uri.split("://")[0]
    uid = uri.split("//")[1].split("@")[0]
    address = uri.split('@')[1].split(":")[0]
    destination_port = int(uri.split(address + ':')[1].split("?")[0])
    network = splitter(uri, "type=")
    security = splitter(uri, "security=")
    sni = splitter(uri, "sni=")
    fp = splitter(uri, "fp=")
    pbk = splitter(uri, "pbk=")

    if "sid=" in uri:
        sid = splitter(uri, "sid=")
    else:
        sid = ""

    if "spx=" in uri:
        spx = splitter(uri, "spx=")
    else:
        spx = ""

    if "flow" in uri:
        flow = splitter(uri, "flow=")
    else:
        flow = ""

    data = {
        "log": {
            "access": "",
            "error": "",
            "loglevel": "warning"
        },
        "outbounds": [
            {
                "tag": "proxy",
                "protocol": protocol,
                "settings": {
                    "vnext": [
                        {
                            "address": address,
                            "port": destination_port,
                            "users": [
                                {
                                    "id": uid,
                                    "alterId": 0,
                                    "email": "t@t.tt",
                                    "security": "auto",
                                    "encryption": "none",
                                    "flow": flow
                                }
                            ]
                        }
                    ]
                },
                "streamSettings": {
                    "network": network,
                    "security": security,
                    "realitySettings": {
                        "serverName": sni,
                        "fingerprint": fp,
                        "show": False,
                        "publicKey": pbk,
                        "shortId": sid,
                        "spiderX": spx
                    }
                },
                "mux": {
                    "enabled": False,
                    "concurrency": -1
                }
            },
            {
                "tag": "direct",
                "protocol": "freedom",
                "settings": {}
            },
            {
                "tag": "block",
                "protocol": "blackhole",
                "settings": {
                    "response": {
                        "type": "http"
                    }
                }
            }
        ]
    }

    if "host=" in uri:
        host_http = splitter(uri, "host=")

        headertype = "http"

        if "headertype" in uri:
            headertype = splitter(uri, "headertype=")

        path = ["/"]
        if "path=" in uri:
            path = [splitter(uri, "path=")]

        headers = {
            "tcpSettings": {
                "header": {
                    "type": headertype,
                    "request": {
                        "version": "1.1",
                        "method": "GET",
                        "path": path,
                        "headers": {
                            "Host": [
                                host_http
                            ],
                            "User-Agent": [
                                ""
                            ],
                            "Accept-Encoding": [
                                "gzip, deflate"
                            ],
                            "Connection": [
                                "keep-alive"
                            ],
                            "Pragma": "no-cache"
                        }
                    }
                }
            }
        }
        data['outbounds'][0]['streamSettings'].update(headers)

    if network == "grpc":
        serviceName = ""
        if "serviceName=" in uri:
            serviceName = splitter(uri, "serviceName=")
        new_dict = {
            "grpcSettings": {
                "serviceName": serviceName,
                "multiMode": False,
                "idle_timeout": 60,
                "health_check_timeout": 20,
                "permit_without_stream": False,
                "initial_windows_size": 0
            }
        }
        data['outbounds'][0]['streamSettings'].update(new_dict)

    data.update(inbound_generator(host, port, socksport))

    json_file_maker(data)  # Simply call the function to print the JSON


def convert_uri_vless_ws_json(host, port, socksport, uri):

    protocol = uri.split("://")[0]
    uid = uri.split("//")[1].split("@")[0]
    address = uri.split('@')[1].split(":")[0]
    destination_port = int(uri.split(address + ':')[1].split("?")[0])
    network = splitter(uri, "type=")
    headers = {}
    if "host=" in uri:
        host_http = splitter(uri, "host=")
        headers = {"Host": host_http}
    if "path=" in uri:
        path = splitter(uri, "path=")

    data = {
        "log": {
            "access": "",
            "error": "",
            "loglevel": "warning"
        },
        "outbounds": [
            {
                "tag": "proxy",
                "protocol": protocol,
                "settings": {
                    "vnext": [
                        {
                            "address": address,
                            "port": destination_port,
                            "users": [
                                {
                                    "id": uid,
                                    "alterId": 0,
                                    "email": "t@t.tt",
                                    "security": "auto",
                                    "encryption": "none",
                                    "flow": ""
                                }
                            ]
                        }
                    ]
                },
                "streamSettings": {
                    "network": network,
                    "wsSettings": {
                        "path": path,
                        "headers": headers
                    }
                },
                "mux": {
                    "enabled": False,
                    "concurrency": -1
                }
            },
            {
                "tag": "direct",
                "protocol": "freedom",
                "settings": {}
            },
            {
                "tag": "block",
                "protocol": "blackhole",
                "settings": {
                    "response": {
                        "type": "http"
                    }
                }
            }
        ]
    }
    if "security=" in uri:
        security = splitter(uri, "security=")
        if security != "none":
            sni = ""
            if "sni=" in uri:
                sni = splitter(uri, "sni=")
            alpn = []
            if "alpn=" in uri:
                alpn_c = splitter(uri, "alpn=")
                if "http/1.1" in alpn_c:
                    alpn.append("http/1.1")
                if "h2" in alpn_c:
                    alpn.append("h2")
                if "h3" in alpn_c:
                    alpn.append("h3")
            new_dict = {
                "security": security,
                "tlsSettings": {
                    "allowInsecure": True,
                    "serverName": sni,
                    "alpn": alpn,
                    "show": False
                }
            }
            data['outbounds'][0]['streamSettings'].update(new_dict)

    data.update(inbound_generator(host, port, socksport))

    return json_file_maker(data)


def convert_uri_vless_tcp_json(host, port, socksport, uri):

    protocol = uri.split("://")[0]
    uid = uri.split("//")[1].split("@")[0]
    address = uri.split('@')[1].split(":")[0]
    destination_port = int(uri.split(address + ':')[1].split("?")[0])
    network = splitter(uri, "type=")

    data = {
        "log": {
            "access": "",
            "error": "",
            "loglevel": "warning"
        },
        "outbounds": [
            {
                "tag": "proxy",
                "protocol": protocol,
                "settings": {
                    "vnext": [
                        {
                            "address": address,
                            "port": destination_port,
                            "users": [
                                {
                                    "id": uid,
                                    "alterId": 0,
                                    "email": "t@t.tt",
                                    "security": "auto",
                                    "encryption": "none",
                                    "flow": ""
                                }
                            ]
                        }
                    ]
                },
                "streamSettings": {
                    "network": network
                },
                "mux": {
                    "enabled": False,
                    "concurrency": -1
                }
            },
            {
                "tag": "direct",
                "protocol": "freedom",
                "settings": {}
            },
            {
                "tag": "block",
                "protocol": "blackhole",
                "settings": {
                    "response": {
                        "type": "http"
                    }
                }
            }
        ]
    }

    if "host=" in uri:
        host_http = splitter(uri, "host=")

        headertype = "http"

        if "headertype" in uri:
            headertype = splitter(uri, "headertype=")

        path = ["/"]
        if "path=" in uri:
            path = [splitter(uri, "path=")]

        headers = {
            "tcpSettings": {
                "header": {
                    "type": headertype,
                    "request": {
                        "version": "1.1",
                        "method": "GET",
                        "path": path,
                        "headers": {
                            "Host": [
                                host_http
                            ],
                            "User-Agent": [
                                ""
                            ],
                            "Accept-Encoding": [
                                "gzip, deflate"
                            ],
                            "Connection": [
                                "keep-alive"
                            ],
                            "Pragma": "no-cache"
                        }
                    }
                }
            }
        }
        data['outbounds'][0]['streamSettings'].update(headers)

    if "security=" in uri:
        security = splitter(uri, "security=")
        if security != "none":
            sni = ""
            if "sni=" in uri:
                sni = splitter(uri, "sni=")
            alpn = []
            if "alpn=" in uri:
                alpn_c = splitter(uri, "alpn=")
                if "http/1.1" in alpn_c:
                    alpn.append("http/1.1")
                if "h2" in alpn_c:
                    alpn.append("h2")
                if "h3" in alpn_c:
                    alpn.append("h3")
            new_dict = {
                "security": security,
                "tlsSettings": {
                    "allowInsecure": True,
                    "serverName": sni,
                    "alpn": alpn,
                    "show": False
                }
            }
            if "fp=" in uri:
                fp = splitter(uri, "fp=")
                if fp != "none":
                    new_dict['tlsSettings'].update({"fingerprint": fp})
            data['outbounds'][0]['streamSettings'].update(new_dict)

    if network == "grpc":
        serviceName = ""
        if "serviceName=" in uri:
            serviceName = splitter(uri, "serviceName=")
        new_dict = {
            "grpcSettings": {
                "serviceName": serviceName,
                "multiMode": False,
                "idle_timeout": 60,
                "health_check_timeout": 20,
                "permit_without_stream": False,
                "initial_windows_size": 0
            }
        }
        data['outbounds'][0]['streamSettings'].update(new_dict)

    data.update(inbound_generator(host, port, socksport))

    return json_file_maker(data)


def convert_uri_vmess_ws_json(host, port, socksport, uri):

    decoded = json.loads(base64.b64decode(uri.split("://")[1]).decode())

    protocol = uri.split("://")[0]
    uid = decoded['id']
    address = decoded['add']
    destination_port = int(decoded['port'])
    network = decoded['net']

    headers = {}
    if decoded.get("host", None) is not None:
        host_http = decoded['host']
        headers = {"Host": host_http}

    path = "/"
    if decoded.get("path", None) is not None:
        path = decoded['path']

    data = {
        "log": {
            "access": "",
            "error": "",
            "loglevel": "warning"
        },
        "outbounds": [
            {
                "tag": "proxy",
                "protocol": protocol,
                "settings": {
                    "vnext": [
                        {
                            "address": address,
                            "port": destination_port,
                            "users": [
                                {
                                    "id": uid,
                                    "alterId": 0,
                                    "email": "t@t.tt",
                                    "security": "auto"
                                }
                            ]
                        }
                    ]
                },
                "streamSettings": {
                    "network": network,
                    "wsSettings": {
                        "path": path,
                        "headers": headers
                    }
                },
                "mux": {
                    "enabled": False,
                    "concurrency": -1
                }
            },
            {
                "tag": "direct",
                "protocol": "freedom",
                "settings": {}
            },
            {
                "tag": "block",
                "protocol": "blackhole",
                "settings": {
                    "response": {
                        "type": "http"
                    }
                }
            }
        ]
    }

    if decoded.get("tls", None) is not None:
        if decoded['tls'].lower() != "none":
            security = decoded['tls'].lower()
            sni = ""
            if decoded.get("sni", None) is not None:
                sni = decoded['sni']
            alpn = []
            if decoded.get("alpn", None) is not None:
                alpn_c = decoded['alpn']
                if "http/1.1" in alpn_c:
                    alpn.append("http/1.1")
                if "h2" in alpn_c:
                    alpn.append("h2")
                if "h3" in alpn_c:
                    alpn.append("h3")

            new_dict = {
                "security": security,
                "tlsSettings": {
                    "allowInsecure": True,
                    "serverName": sni,
                    "alpn": alpn,
                    "show": False
                }
            }
            if decoded.get("fp", None) is not None:
                fp = decoded['fp']
                if fp != "none":
                    new_dict['tlsSettings'].update({"fingerprint": fp})
            data['outbounds'][0]['streamSettings'].update(new_dict)

    data.update(inbound_generator(host, port, socksport))

    return json_file_maker(data)


def convert_uri_vmess_tcp_json(host, port, socksport, uri):

    decoded = json.loads(base64.b64decode(uri.split("://")[1]).decode())

    protocol = uri.split("://")[0]
    uid = decoded['id']
    address = decoded['add']
    destination_port = int(decoded['port'])
    network = decoded['net']

    data = {
        "log": {
            "access": "",
            "error": "",
            "loglevel": "warning"
        },
        "outbounds": [
            {
                "tag": "proxy",
                "protocol": protocol,
                "settings": {
                    "vnext": [
                        {
                            "address": address,
                            "port": destination_port,
                            "users": [
                                {
                                    "id": uid,
                                    "alterId": 0,
                                    "email": "t@t.tt",
                                    "security": "auto"
                                }
                            ]
                        }
                    ]
                },
                "streamSettings": {
                    "network": network
                },
                "mux": {
                    "enabled": False,
                    "concurrency": -1
                }
            },
            {
                "tag": "direct",
                "protocol": "freedom",
                "settings": {}
            },
            {
                "tag": "block",
                "protocol": "blackhole",
                "settings": {
                    "response": {
                        "type": "http"
                    }
                }
            }
        ]
    }

    headers = {}
    if decoded.get("host", None) is not None:
        host_http = decoded['host']
        if host_http != "":
            headers = {"Host": host_http}

            headertype = "http"
            if decoded.get("type", None) is not None:
                headertype = decoded['type']

            path = ['/']
            if decoded.get("path", None) is not None:
                path = [decoded['path']]

            headers = {
                "tcpSettings": {
                    "header": {
                        "type": headertype,
                        "request": {
                            "version": "1.1",
                            "method": "GET",
                            "path": path,
                            "headers": {
                                "Host": [
                                    host_http
                                ],
                                "User-Agent": [
                                    ""
                                ],
                                "Accept-Encoding": [
                                    "gzip, deflate"
                                ],
                                "Connection": [
                                    "keep-alive"
                                ],
                                "Pragma": "no-cache"
                            }
                        }
                    }
                }
            }
            data['outbounds'][0]['streamSettings'].update(headers)

    if decoded.get("tls", None) is not None:
        if decoded['tls'].lower() not in ["none", ""]:
            security = decoded['tls'].lower()
            sni = ""
            if decoded.get("sni", None) is not None:
                sni = decoded['sni']
            if decoded.get("alpn", None) is not None:
                alpn_c = decoded['alpn']
                alpn = []
                if "http/1.1" in alpn_c:
                    alpn.append("http/1.1")
                if "h2" in alpn_c:
                    alpn.append("h2")
                if "h3" in alpn_c:
                    alpn.append("h3")

            new_dict = {
                "security": security,
                "tlsSettings": {
                    "allowInsecure": True,
                    "serverName": sni,
                    "alpn": alpn,
                    "show": False
                }
            }
            if decoded.get("fp", None) is not None:
                fp = decoded['fp']
                if fp != "none":
                    new_dict['tlsSettings'].update({"fingerprint": fp})
            data['outbounds'][0]['streamSettings'].update(new_dict)

    if network == "grpc":
        serviceName = ""
        if decoded.get("path", None) is not None:
            serviceName = decoded['path']
        new_dict = {
            "grpcSettings": {
                "serviceName": serviceName,
                "multiMode": False,
                "idle_timeout": 60,
                "health_check_timeout": 20,
                "permit_without_stream": False,
                "initial_windows_size": 0
            }
        }
        data['outbounds'][0]['streamSettings'].update(new_dict)

    data.update(inbound_generator(host, port, socksport))

    return json_file_maker(data)


def convert_uri_trojan_reality_json(host, port, socksport, uri):

    protocol = uri.split("://")[0]
    password = uri.split("//")[1].split("@")[0]
    address = uri.split('@')[1].split(":")[0]
    destination_port = int(uri.split(address + ':')[1].split("?")[0])
    network = splitter(uri, "type=")

    security = splitter(uri, "security=")
    sni = splitter(uri, "sni=")
    fp = splitter(uri, "fp=")
    pbk = splitter(uri, "pbk=")

    if "sid=" in uri:
        sid = splitter(uri, "sid=")
    else:
        sid = ""

    if "spx=" in uri:
        spx = splitter(uri, "spx=")
    else:
        spx = ""

    if "flow" in uri:
        flow = splitter(uri, "flow=")
    else:
        flow = ""

    data = {
        "log": {
            "access": "",
            "error": "",
            "loglevel": "warning"
        },
        "outbounds": [
            {
                "tag": "proxy",
                "protocol": protocol,
                "settings": {
                    "servers": [
                        {
                            "address": address,
                            "method": "chacha20",
                            "ota": False,
                            "password": password,
                            "port": destination_port,
                            "level": 1,
                            "flow": ""
                        }
                    ]
                },
                "streamSettings": {
                    "network": network,
                    "security": security,
                    "realitySettings": {
                        "serverName": sni,
                        "fingerprint": fp,
                        "show": False,
                        "publicKey": pbk,
                        "shortId": sid,
                        "spiderX": spx
                    }
                },
                "mux": {
                    "enabled": False,
                    "concurrency": -1
                }
            },
            {
                "tag": "direct",
                "protocol": "freedom",
                "settings": {}
            },
            {
                "tag": "block",
                "protocol": "blackhole",
                "settings": {
                    "response": {
                        "type": "http"
                    }
                }
            }
        ]
    }

    if "host=" in uri:
        host_http = splitter(uri, "host=")

        headertype = "http"

        if "headertype" in uri:
            headertype = splitter(uri, "headertype=")

        path = ["/"]
        if "path=" in uri:
            path = [splitter(uri, "path=")]

        headers = {
            "tcpSettings": {
                "header": {
                    "type": headertype,
                    "request": {
                        "version": "1.1",
                        "method": "GET",
                        "path": path,
                        "headers": {
                            "Host": [
                                host_http
                            ],
                            "User-Agent": [
                                ""
                            ],
                            "Accept-Encoding": [
                                "gzip, deflate"
                            ],
                            "Connection": [
                                "keep-alive"
                            ],
                            "Pragma": "no-cache"
                        }
                    }
                }
            }
        }
        data['outbounds'][0]['streamSettings'].update(headers)

    if network == "grpc":
        serviceName = ""
        if "serviceName=" in uri:
            serviceName = splitter(uri, "serviceName=")
        new_dict = {
            "grpcSettings": {
                "serviceName": serviceName,
                "multiMode": False,
                "idle_timeout": 60,
                "health_check_timeout": 20,
                "permit_without_stream": False,
                "initial_windows_size": 0
            }
        }
        data['outbounds'][0]['streamSettings'].update(new_dict)

    data.update(inbound_generator(host, port, socksport))

    return json_file_maker(data)


def convert_uri_trojan_ws_json(host, port, socksport, uri):

    protocol = uri.split("://")[0]
    password = uri.split("//")[1].split("@")[0]
    address = uri.split('@')[1].split(":")[0]
    destination_port = int(uri.split(address + ':')[1].split("?")[0])
    network = splitter(uri, "type=")
    headers = {}
    if "host=" in uri:
        host_http = splitter(uri, "host=")
        headers = {"Host": host_http}

    path = "/"
    if "path=" in uri:
        path = splitter(uri, "path=")

    data = {
        "log": {
            "access": "",
            "error": "",
            "loglevel": "warning"
        },
        "outbounds": [
            {
                "tag": "proxy",
                "protocol": protocol,
                "settings": {
                    "servers": [
                        {
                            "address": address,
                            "method": "chacha20",
                            "ota": False,
                            "password": password,
                            "port": destination_port,
                            "level": 1,
                            "flow": ""
                        }
                    ]
                },
                "streamSettings": {
                    "network": network,
                    "wsSettings": {
                        "path": path,
                        "headers": headers
                    }
                },
                "mux": {
                    "enabled": False,
                    "concurrency": -1
                }
            },
            {
                "tag": "direct",
                "protocol": "freedom",
                "settings": {}
            },
            {
                "tag": "block",
                "protocol": "blackhole",
                "settings": {
                    "response": {
                        "type": "http"
                    }
                }
            }
        ]
    }
    if "security=" in uri:
        security = splitter(uri, "security=")
        if security != "none":
            sni = ""
            if "sni=" in uri:
                sni = splitter(uri, "sni=")
            alpn = []
            if "alpn=" in uri:
                alpn_c = splitter(uri, "alpn=")
                if "http/1.1" in alpn_c:
                    alpn.append("http/1.1")
                if "h2" in alpn_c:
                    alpn.append("h2")
                if "h3" in alpn_c:
                    alpn.append("h3")
            new_dict = {
                "security": security,
                "tlsSettings": {
                    "allowInsecure": True,
                    "serverName": sni,
                    "alpn": alpn,
                    "show": False
                }
            }
            data['outbounds'][0]['streamSettings'].update(new_dict)

    data.update(inbound_generator(host, port, socksport))

    return json_file_maker(data)


def convert_uri_trojan_tcp_json(host, port, socksport, uri):

    protocol = uri.split("://")[0]
    password = uri.split("//")[1].split("@")[0]
    address = uri.split('@')[1].split(":")[0]
    destination_port = int(uri.split(address + ':')[1].split("?")[0])
    network = splitter(uri, "type=")
    data = {
        "log": {
            "access": "",
            "error": "",
            "loglevel": "warning"
        },
        "outbounds": [
            {
                "tag": "proxy",
                "protocol": protocol,
                "settings": {
                    "servers": [
                        {
                            "address": address,
                            "method": "chacha20",
                            "ota": False,
                            "password": password,
                            "port": destination_port,
                            "level": 1,
                            "flow": ""
                        }
                    ]
                },
                "streamSettings": {
                    "network": network
                },
                "mux": {
                    "enabled": False,
                    "concurrency": -1
                }
            },
            {
                "tag": "direct",
                "protocol": "freedom",
                "settings": {}
            },
            {
                "tag": "block",
                "protocol": "blackhole",
                "settings": {
                    "response": {
                        "type": "http"
                    }
                }
            }
        ]
    }

    if "host=" in uri:
        host_http = splitter(uri, "host=")

        headertype = "http"

        if "headertype" in uri.lower():
            headertype = splitter(uri.lower(), "headertype=")

        path = ["/"]
        if "path=" in uri:
            path = [splitter(uri, "path=")]

        headers = {
            "tcpSettings": {
                "header": {
                    "type": headertype,
                    "request": {
                        "version": "1.1",
                        "method": "GET",
                        "path": path,
                        "headers": {
                            "Host": [
                                host_http
                            ],
                            "User-Agent": [
                                ""
                            ],
                            "Accept-Encoding": [
                                "gzip, deflate"
                            ],
                            "Connection": [
                                "keep-alive"
                            ],
                            "Pragma": "no-cache"
                        }
                    }
                }
            }
        }
        data['outbounds'][0]['streamSettings'].update(headers)

    if "security=" in uri:
        security = splitter(uri, "security=")
        if security != "none":
            sni = ""
            if "sni=" in uri:
                sni = splitter(uri, "sni=")
            alpn = []
            if "alpn=" in uri:
                alpn_c = splitter(uri, "alpn=")
                if "http/1.1" in alpn_c:
                    alpn.append("http/1.1")
                if "h2" in alpn_c:
                    alpn.append("h2")
                if "h3" in alpn_c:
                    alpn.append("h3")
            new_dict = {
                "security": security,
                "tlsSettings": {
                    "allowInsecure": True,
                    "serverName": sni,
                    "alpn": alpn,
                    "show": False
                }
            }
            if "fp=" in uri:
                fp = splitter(uri, "fp=")
                if fp != "none":
                    new_dict['tlsSettings'].update({"fingerprint": fp})
            data['outbounds'][0]['streamSettings'].update(new_dict)

    if network == "grpc":
        serviceName = ""
        if "serviceName=" in uri:
            serviceName = splitter(uri, "serviceName=")
        new_dict = {
            "grpcSettings": {
                "serviceName": serviceName,
                "multiMode": False,
                "idle_timeout": 60,
                "health_check_timeout": 20,
                "permit_without_stream": False,
                "initial_windows_size": 0
            }
        }

    data.update(inbound_generator(host, port, socksport))

    return json_file_maker(data)


def Vless_Reality_checker(uri):
    if "security=" in uri and "vless://" in uri:
        if uri.split("security=")[1].split("&")[0] == "reality":
            return True
    return False


def vless_ws_checker(uri):
    if "type=ws" in uri and "vless://" in uri:
        return True
    else:
        return False


def vless_tcp_checker(uri):
    if ("type=tcp" in uri or "type=grpc" in uri) and "vless://" in uri:
        return True
    else:
        return False


def vmess_ws_checker(uri):
    if "vmess://" in uri:
        decoded = json.loads(base64.b64decode(uri.split("://")[1]).decode())
        if "ws" == decoded['net']:
            return True
    return False


def vmess_tcp_checker(uri):
    if "vmess://" in uri:
        decoded = json.loads(base64.b64decode(uri.split("://")[1]).decode())
        if ("tcp" == decoded['net']) or ("grpc" == decoded['net']):
            return True
    return False


def trojan_Reality_checker(uri):
    if "security=" in uri and "trojan://" in uri:
        if uri.split("security=")[1].split("&")[0] == "reality":
            return True
    return False


def trojan_ws_checker(uri):
    if "type=ws" in uri and "trojan://" in uri:
        return True
    else:
        return False


def trojan_tcp_checker(uri):
    if ("type=tcp" in uri or "type=grpc" in uri) and "trojan://" in uri:
        return True
    else:
        return False


def convert_uri_json(host="127.0.0.1", port=10809, socksport=10808, uri=None):
    if uri is None:
        return False
    uri = uri.replace("%2F", "/")

    if Vless_Reality_checker(uri) is True:
        convert_uri_reality_json(host, port, socksport, uri)
    elif vless_ws_checker(uri) is True:
        convert_uri_vless_ws_json(host, port, socksport, uri)
    elif vless_tcp_checker(uri) is True:
        convert_uri_vless_tcp_json(host, port, socksport, uri)
    elif vmess_ws_checker(uri) is True:
        convert_uri_vmess_ws_json(host, port, socksport, uri)
    elif vmess_tcp_checker(uri) is True:
        convert_uri_vmess_tcp_json(host, port, socksport, uri)
    elif trojan_Reality_checker(uri) is True:
        convert_uri_trojan_reality_json(host, port, socksport, uri)
    elif trojan_ws_checker(uri) is True:
        convert_uri_trojan_ws_json(host, port, socksport, uri)
    elif trojan_tcp_checker(uri) is True:
        convert_uri_trojan_tcp_json(host, port, socksport, uri)

if __name__ == "__main__":
    import sys
    uri = sys.argv[1]
    convert_uri_json(uri=uri)  # JSON will print directly to the terminal
