---
description: GitHub Repo Contains Test Files.
hidden: true
---

# Jitsi Meet Test Files

### THIS IS IN TESTING, USE AT YOUR OWN RISK.

For trying to get Jitsi meet to pass through Authentik correctly when Authentik is the reverse proxy.

{% code expandable="true" %}
```py
#################
# Domain Policy 1 #
#################

def policy_function(domain, room, muc_room_domain, shard):
    """Production-ready policy function for Jitsi Meet deployment"""
    
    # List of all allowed domains
    allowed_domains = [
        "meet.YOUR.DOMAIN",
        "auth.meet.YOUR.DOMAIN",
        "guest.meet.YOUR.DOMAIN",
        "muc.meet.YOUR.DOMAIN",
        "recorder.meet.YOUR.DOMAIN"
    ]
    
    # IP address fallback
    ip_fallback = "LOCAL.IP.ADDRESS:8001"
    
    # Handle SSL_ERROR_NO_CYPHER_OVERLAP by providing alternative endpoints
    if domain in allowed_domains:
        # Main domain handling
        if domain == "meet.YOUR.DOMAIN":
            return {
                "bosh": f"//{domain}/http-bind",
                "websocket": f"wss://{domain}/xmpp-websocket",
                "focus": f"focus.{domain}",
                "muc": f"muc.{domain}"
            }
        
        # Special handling for auth domain
        elif domain == "auth.meet.YOUR.DOMAIN":
            return {
                "bosh": f"//{domain}/http-bind",
                "websocket": f"wss://{domain}/xmpp-websocket",
                "anonymous": False
            }
        
        # Guest domain handling
        elif domain == "guest.meet.YOUR.DOMAIN":
            return {
                "bosh": f"//{domain}/http-bind",
                "websocket": f"wss://{domain}/xmpp-websocket",
                "anonymous": True
            }
        
        # MUC domain handling
        elif domain == "muc.meet.YOUR.DOMAIN":
            return {
                "bosh": f"//{domain}/http-bind",
                "websocket": f"wss://{domain}/xmpp-websocket",
                "muc": f"conference.{domain}"
            }
        
        # Recorder domain handling
        elif domain == "recorder.meet.YOUR.DOMAIN":
            return {
                "bosh": f"//{domain}/http-bind",
                "websocket": f"wss://{domain}/xmpp-websocket",
                "focus": f"focus.{domain}",
                "disableRtx": True
            }
    
    # Fallback to IP address if domain resolution fails or for local testing
    return {
        "bosh": f"//{ip_fallback}/http-bind",
        "websocket": f"ws://{ip_fallback}/xmpp-websocket",
        "focus": f"focus.{ip_fallback}",
        "muc": f"conference.{ip_fallback}"
    }
```
{% endcode %}

{% code expandable="true" %}
```py
#################
# Domain Policy 2 #
#################

def policy_function(domain, room, muc_room_domain, shard):
    """Advanced Jitsi Meet policy with port forwarding based on env.yml"""
    
    # Load configuration from env.yml (simulated here as a dict)
    config = {
        "HTTP_PORT": 8001,
        "HTTPS_PORT": 8443,
        "JVB_PORT": 10001,
        "JVB_COLIBRI_PORT": 8080,
        "COLIBRI_WEBSOCKET_PORT": 9090,
        "PUBLIC_URL": "https://meet.YOUR.DOMAIN",
        "XMPP_DOMAIN": "meet.YOUR.DOMAIN",
        "XMPP_AUTH_DOMAIN": "auth.meet.YOUR.DOMAIN",
        "XMPP_GUEST_DOMAIN": "guest.meet.YOUR.DOMAIN",
        "XMPP_MUC_DOMAIN": "muc.meet.YOUR.DOMAIN",
        "XMPP_RECORDER_DOMAIN": "recorder.meet.YOUR.DOMAIN",
        "IP_FALLBACK": "192.168.0.0" # ENTER LOCAL IP OF JITSI
    }

    # Allowed domains (from env.yml)
    allowed_domains = [
        config["XMPP_DOMAIN"],
        config["XMPP_AUTH_DOMAIN"],
        config["XMPP_GUEST_DOMAIN"],
        config["XMPP_MUC_DOMAIN"],
        config["XMPP_RECORDER_DOMAIN"]
    ]

    # Port mappings for services
    port_mappings = {
        "bosh": config["HTTP_PORT"],
        "websocket": config["HTTPS_PORT"],
        "jvb": config["JVB_PORT"],
        "colibri": config["JVB_COLIBRI_PORT"],
        "colibri_websocket": config["COLIBRI_WEBSOCKET_PORT"]
    }

    # Domain-based routing with port forwarding
    if domain in allowed_domains:
        # Main domain handling
        if domain == config["XMPP_DOMAIN"]:
            return {
                "bosh": f"//{domain}:{port_mappings['bosh']}/http-bind",
                "websocket": f"wss://{domain}:{port_mappings['websocket']}/xmpp-websocket",
                "focus": f"focus.{domain}:{port_mappings['websocket']}",
                "muc": f"muc.{domain}:{port_mappings['websocket']}",
                "jvb": f"jvb.{domain}:{port_mappings['jvb']}",
                "colibri": f"colibri.{domain}:{port_mappings['colibri']}",
                "disableRtx": False
            }
        
        # Auth domain handling
        elif domain == config["XMPP_AUTH_DOMAIN"]:
            return {
                "bosh": f"//{domain}:{port_mappings['bosh']}/http-bind",
                "websocket": f"wss://{domain}:{port_mappings['websocket']}/xmpp-websocket",
                "anonymous": False,
                "jvb": f"jvb.{domain}:{port_mappings['jvb']}"
            }
        
        # Guest domain handling
        elif domain == config["XMPP_GUEST_DOMAIN"]:
            return {
                "bosh": f"//{domain}:{port_mappings['bosh']}/http-bind",
                "websocket": f"wss://{domain}:{port_mappings['websocket']}/xmpp-websocket",
                "anonymous": True,
                "colibri_websocket": f"wss://{domain}:{port_mappings['colibri_websocket']}/colibri-ws"
            }
        
        # MUC domain handling
        elif domain == config["XMPP_MUC_DOMAIN"]:
            return {
                "bosh": f"//{domain}:{port_mappings['bosh']}/http-bind",
                "websocket": f"wss://{domain}:{port_mappings['websocket']}/xmpp-websocket",
                "muc": f"conference.{domain}:{port_mappings['websocket']}",
                "colibri": f"colibri.{domain}:{port_mappings['colibri']}"
            }
        
        # Recorder domain handling
        elif domain == config["XMPP_RECORDER_DOMAIN"]:
            return {
                "bosh": f"//{domain}:{port_mappings['bosh']}/http-bind",
                "websocket": f"wss://{domain}:{port_mappings['websocket']}/xmpp-websocket",
                "focus": f"focus.{domain}:{port_mappings['websocket']}",
                "disableRtx": True,
                "jvb": f"jvb.{domain}:{port_mappings['jvb']}"
            }
    
    # Fallback to IP and default ports (for local/dev environments)
    return {
        "bosh": f"//{config['IP_FALLBACK']}:{port_mappings['bosh']}/http-bind",
        "websocket": f"ws://{config['IP_FALLBACK']}:{port_mappings['websocket']}/xmpp-websocket",
        "focus": f"focus.{config['IP_FALLBACK']}:{port_mappings['websocket']}",
        "muc": f"conference.{config['IP_FALLBACK']}:{port_mappings['websocket']}",
        "jvb": f"{config['IP_FALLBACK']}:{port_mappings['jvb']}",
        "colibri": f"{config['IP_FALLBACK']}:{port_mappings['colibri']}"
    }
```
{% endcode %}

{% code expandable="true" %}
```py
#################
# Domain Policy 3 #
#################

def policy_function(domain, room, muc_room_domain, shard):
    """Production-ready policy function for Jitsi Meet deployment with port forwarding"""
    
    # Load configuration from env.yml (simulated here as a dict)
    config = {
        "HTTP_PORT": 8001,
        "HTTPS_PORT": 8443,
        "JVB_PORT": 10001,
        "JVB_COLIBRI_PORT": 8080,
        "COLIBRI_WEBSOCKET_PORT": 9090,
        "PUBLIC_URL": "https://meet.YOUR.DOMAIN",
        "XMPP_DOMAIN": "meet.YOUR.DOMAIN",
        "XMPP_AUTH_DOMAIN": "auth.meet.YOUR.DOMAIN",
        "XMPP_GUEST_DOMAIN": "guest.meet.YOUR.DOMAIN",
        "XMPP_MUC_DOMAIN": "muc.meet.YOUR.DOMAIN",
        "XMPP_RECORDER_DOMAIN": "recorder.meet.YOUR.DOMAIN"
    }

    # Allowed domains (from env.yml)
    allowed_domains = [
        config["XMPP_DOMAIN"],
        config["XMPP_AUTH_DOMAIN"],
        config["XMPP_GUEST_DOMAIN"],
        config["XMPP_MUC_DOMAIN"],
        config["XMPP_RECORDER_DOMAIN"]
    ]

    # Port forwarding rules (service: external_port → internal_port)
    port_forwarding = {
        "http": {"external": config["HTTP_PORT"], "internal": 80},
        "https": {"external": config["HTTPS_PORT"], "internal": 443},
        "jvb": {"external": config["JVB_PORT"], "internal": 10000},
        "colibri": {"external": config["JVB_COLIBRI_PORT"], "internal": 8080},
        "colibri_websocket": {"external": config["COLIBRI_WEBSOCKET_PORT"], "internal": 9090}
    }

    # Domain-specific routing + port forwarding
    if domain in allowed_domains:
        # Main domain (meet.YOUR.DOMAIN)
        if domain == config["XMPP_DOMAIN"]:
            return {
                "bosh": f"//{domain}:{config['HTTPS_PORT']}/http-bind",
                "websocket": f"wss://{domain}:{config['HTTPS_PORT']}/xmpp-websocket",
                "focus": f"focus.{domain}",
                "muc": f"muc.{domain}",
                "ports": {
                    "http": port_forwarding["http"],
                    "https": port_forwarding["https"],
                    "jvb": port_forwarding["jvb"]
                }
            }
        
        # Auth domain (auth.meet.YOUR.DOMAIN)
        elif domain == config["XMPP_AUTH_DOMAIN"]:
            return {
                "bosh": f"//{domain}:{config['HTTPS_PORT']}/http-bind",
                "websocket": f"wss://{domain}:{config['HTTPS_PORT']}/xmpp-websocket",
                "anonymous": False,
                "ports": {
                    "https": port_forwarding["https"],
                    "colibri": port_forwarding["colibri"]
                }
            }
        
        # Guest domain (guest.meet.YOUR.DOMAIN)
        elif domain == config["XMPP_GUEST_DOMAIN"]:
            return {
                "bosh": f"//{domain}:{config['HTTPS_PORT']}/http-bind",
                "websocket": f"wss://{domain}:{config['HTTPS_PORT']}/xmpp-websocket",
                "anonymous": True,
                "ports": {
                    "https": port_forwarding["https"],
                    "colibri_websocket": port_forwarding["colibri_websocket"]
                }
            }
        
        # MUC domain (muc.meet.YOUR.DOMAIN)
        elif domain == config["XMPP_MUC_DOMAIN"]:
            return {
                "bosh": f"//{domain}:{config['HTTPS_PORT']}/http-bind",
                "websocket": f"wss://{domain}:{config['HTTPS_PORT']}/xmpp-websocket",
                "muc": f"conference.{domain}",
                "ports": {
                    "https": port_forwarding["https"],
                    "jvb": port_forwarding["jvb"]
                }
            }
        
        # Recorder domain (recorder.meet.YOUR.DOMAIN)
        elif domain == config["XMPP_RECORDER_DOMAIN"]:
            return {
                "bosh": f"//{domain}:{config['HTTPS_PORT']}/http-bind",
                "websocket": f"wss://{domain}:{config['HTTPS_PORT']}/xmpp-websocket",
                "focus": f"focus.{domain}",
                "disableRtx": True,
                "ports": {
                    "https": port_forwarding["https"],
                    "colibri": port_forwarding["colibri"]
                }
            }
    
    # Fallback for invalid domains
    return {
        "error": "Domain not allowed",
        "allowed_domains": allowed_domains
    }
```
{% endcode %}

{% code expandable="true" %}
```py
#################
# Domain Policy 4 #
#################

def policy_function(domain, room, muc_room_domain, shard):
    """Advanced Jitsi Meet policy with port forwarding, reverse proxy rules, and mobile optimizations."""
    
    # Load config from env.yml (simplified for policy; real impl. would parse YAML)
    CONFIG = {
        "HTTP_PORT": 8001,
        "HTTPS_PORT": 8443,
        "JVB_PORT": 10001,
        "COLIBRI_WEBSOCKET_PORT": 9090,
        "PUBLIC_URL": "https://meet.YOUR.DOMAIN",
        "XMPP_DOMAIN": "meet.YOUR.DOMAIN",
        "XMPP_AUTH_DOMAIN": "auth.meet.YOUR.DOMAIN",
        "XMPP_GUEST_DOMAIN": "guest.meet.YOUR.DOMAIN",
        "XMPP_MUC_DOMAIN": "muc.meet.YOUR.DOMAIN",
        "XMPP_RECORDER_DOMAIN": "recorder.meet.YOUR.DOMAIN",
        "ENABLE_AUTH": False,
        "ENABLE_P2P": True,
    }

    # Allowed domains (from env.yml)
    allowed_domains = [
        CONFIG["XMPP_DOMAIN"],
        CONFIG["XMPP_AUTH_DOMAIN"],
        CONFIG["XMPP_GUEST_DOMAIN"],
        CONFIG["XMPP_MUC_DOMAIN"],
        CONFIG["XMPP_RECORDER_DOMAIN"]
    ]

    # Fallback IP (local-only, not exposed to reverse proxy)
    FALLBACK_IP = "192.168.25.87"

    # Mobile-specific fixes (override WebSocket ports for Android/iOS)
    MOBILE_OVERRIDES = {
        "websocket": f"wss://{domain}:{CONFIG['HTTPS_PORT']}/colibri-ws/{room}",
        "useStunTurn": True,  # Force TURN for mobile NAT traversal
        "disableRtx": False,   # Fixes packet loss on mobile networks
        "enableIceRestart": True  # Helps with network switches (WiFi → Cellular)
    }

    # Policy logic
    if domain in allowed_domains:
        # Base config for all domains
        config = {
            "bosh": f"//{domain}:{CONFIG['HTTP_PORT']}/http-bind",
            "websocket": f"wss://{domain}:{CONFIG['HTTPS_PORT']}/xmpp-websocket",
            "hosts": {
                "domain": domain,
                "muc": CONFIG["XMPP_MUC_DOMAIN"],
                "focus": f"focus.{domain}",
            },
            "p2p": {
                "enabled": CONFIG["ENABLE_P2P"],
                "stunServers": [  # Fallback STUN for mobile
                    {"urls": "stun:stun.l.google.com:19302"}
                ]
            },
            # Port forwarding rules (reverse proxy only sees HTTP/HTTPS)
            "ports": {
                "http": CONFIG["HTTP_PORT"],
                "https": CONFIG["HTTPS_PORT"],
                "jvb": CONFIG["JVB_PORT"],  # Local-only (forwarded internally)
                "colibri": CONFIG["COLIBRI_WEBSOCKET_PORT"]  # Local-only
            },
            # Fallback IP (local routing if reverse proxy fails)
            "fallback": {
                "ip": FALLBACK_IP,
                "ports": {
                    "http": CONFIG["HTTP_PORT"],
                    "https": CONFIG["HTTPS_PORT"]
                }
            }
        }

        # Domain-specific overrides
        if domain == CONFIG["XMPP_AUTH_DOMAIN"]:
            config.update({"anonymous": False})
        elif domain == CONFIG["XMPP_GUEST_DOMAIN"]:
            config.update({"anonymous": True})
        elif domain == CONFIG["XMPP_MUC_DOMAIN"]:
            config["hosts"]["muc"] = f"conference.{domain}"
        elif domain == CONFIG["XMPP_RECORDER_DOMAIN"]:
            config.update({"disableRtx": True})

        # Mobile optimizations (applied last to override defaults)
        if "Android" in str(shard) or "iOS" in str(shard):
            config.update(MOBILE_OVERRIDES)

        return config
    else:
        raise ValueError(f"Domain {domain} not allowed")
```
{% endcode %}

{% code expandable="true" %}
```py
###################
# DOMAIN POLICY 5 #
###################

def policy_function(domain, room, muc_room_domain, shard):
    """Jitsi Meet policy with HTTP and WebRTC support only, SSL error mitigation"""
    
    # Load configuration from env.yml (simulated here as a dict)
    config = {
        "HTTP_PORT": 8001,
        "HTTPS_PORT": 8443,
        "JVB_PORT": 10001,
        "JVB_COLIBRI_PORT": 8080,
        "COLIBRI_WEBSOCKET_PORT": 9090,
        "PUBLIC_URL": "http://meet.YOUR.DOMAIN",  # Changed to http
        "XMPP_DOMAIN": "meet.YOUR.DOMAIN",
        "XMPP_AUTH_DOMAIN": "auth.meet.YOUR.DOMAIN",
        "XMPP_GUEST_DOMAIN": "guest.meet.YOUR.DOMAIN",
        "XMPP_MUC_DOMAIN": "muc.meet.YOUR.DOMAIN",
        "XMPP_RECORDER_DOMAIN": "recorder.meet.YOUR.DOMAIN",
        "IP_FALLBACK": "192.168.0.0" # ENTER LOCAL IP OF JITSI
    }

    # Allowed domains (from env.yml)
    allowed_domains = [
        config["XMPP_DOMAIN"],
        config["XMPP_AUTH_DOMAIN"],
        config["XMPP_GUEST_DOMAIN"],
        config["XMPP_MUC_DOMAIN"],
        config["XMPP_RECORDER_DOMAIN"]
    ]

    # Port mappings for services - using HTTP ports where possible
    port_mappings = {
        "bosh": config["HTTP_PORT"],
        "websocket": config["HTTP_PORT"],  # Using HTTP port for WS
        "jvb": config["JVB_PORT"],
        "colibri": config["JVB_COLIBRI_PORT"],
        "colibri_websocket": config["COLIBRI_WEBSOCKET_PORT"]
    }

    # Domain-based routing with port forwarding
    if domain in allowed_domains:
        # Main domain handling
        if domain == config["XMPP_DOMAIN"]:
            return {
                "bosh": f"http://{domain}:{port_mappings['bosh']}/http-bind",  # Explicit http
                "websocket": f"ws://{domain}:{port_mappings['websocket']}/xmpp-websocket",  # ws instead of wss
                "focus": f"focus.{domain}:{port_mappings['websocket']}",
                "muc": f"muc.{domain}:{port_mappings['websocket']}",
                "jvb": f"jvb.{domain}:{port_mappings['jvb']}",
                "colibri": f"colibri.{domain}:{port_mappings['colibri']}",
                "disableRtx": False,
                "enableLipSync": False,
                "openBridgeChannel": "websocket",  # Force websocket for bridge
                "protocols": ["http", "webrtc"],  # Explicitly limit protocols
                "useStunTurn": True,  # Ensure WebRTC works properly
                "disableH264": False
            }
        
        # Auth domain handling
        elif domain == config["XMPP_AUTH_DOMAIN"]:
            return {
                "bosh": f"http://{domain}:{port_mappings['bosh']}/http-bind",
                "websocket": f"ws://{domain}:{port_mappings['websocket']}/xmpp-websocket",
                "anonymous": False,
                "jvb": f"jvb.{domain}:{port_mappings['jvb']}",
                "protocols": ["http", "webrtc"]
            }
        
        # Guest domain handling
        elif domain == config["XMPP_GUEST_DOMAIN"]:
            return {
                "bosh": f"http://{domain}:{port_mappings['bosh']}/http-bind",
                "websocket": f"ws://{domain}:{port_mappings['websocket']}/xmpp-websocket",
                "anonymous": True,
                "colibri_websocket": f"ws://{domain}:{port_mappings['colibri_websocket']}/colibri-ws",
                "protocols": ["http", "webrtc"]
            }
        
        # MUC domain handling
        elif domain == config["XMPP_MUC_DOMAIN"]:
            return {
                "bosh": f"http://{domain}:{port_mappings['bosh']}/http-bind",
                "websocket": f"ws://{domain}:{port_mappings['websocket']}/xmpp-websocket",
                "muc": f"conference.{domain}:{port_mappings['websocket']}",
                "colibri": f"colibri.{domain}:{port_mappings['colibri']}",
                "protocols": ["http", "webrtc"]
            }
        
        # Recorder domain handling
        elif domain == config["XMPP_RECORDER_DOMAIN"]:
            return {
                "bosh": f"http://{domain}:{port_mappings['bosh']}/http-bind",
                "websocket": f"ws://{domain}:{port_mappings['websocket']}/xmpp-websocket",
                "focus": f"focus.{domain}:{port_mappings['websocket']}",
                "disableRtx": True,
                "jvb": f"jvb.{domain}:{port_mappings['jvb']}",
                "protocols": ["http", "webrtc"]
            }
    
    # Fallback to IP and default ports (for local/dev environments)
    return {
        "bosh": f"http://{config['IP_FALLBACK']}:{port_mappings['bosh']}/http-bind",
        "websocket": f"ws://{config['IP_FALLBACK']}:{port_mappings['websocket']}/xmpp-websocket",
        "focus": f"focus.{config['IP_FALLBACK']}:{port_mappings['websocket']}",
        "muc": f"conference.{config['IP_FALLBACK']}:{port_mappings['websocket']}",
        "jvb": f"{config['IP_FALLBACK']}:{port_mappings['jvb']}",
        "colibri": f"{config['IP_FALLBACK']}:{port_mappings['colibri']}",
        "protocols": ["http", "webrtc"],
        "useStunTurn": True
    }
```
{% endcode %}

```py
# Ensure WebSocket (wss://) and BOSH (http-bind) are allowed
if request.path.startswith("/xmpp-websocket") or request.path.startswith("/http-bind"):
    return True  # Allow WebSocket/XMPP traffic
else:
    return request.host == "meet.YOUR.DOMAIN"  # Only allow Jitsi domain
```
