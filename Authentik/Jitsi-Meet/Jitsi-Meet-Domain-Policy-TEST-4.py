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