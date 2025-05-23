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