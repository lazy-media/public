##############################################################
# Ensure WebSocket (wss://) and BOSH (http-bind) are allowed #
##############################################################

if request.path.startswith("/xmpp-websocket") or request.path.startswith("/http-bind"):
    return True  # Allow WebSocket/XMPP traffic
else:
    return request.host == "meet.lazymedia.media"  # Only allow Jitsi domain

#################
# Domain Policy #
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
        "PUBLIC_URL": "https://meet.lazymedia.media",
        "XMPP_DOMAIN": "meet.lazymedia.media",
        "XMPP_AUTH_DOMAIN": "auth.meet.lazymedia.media",
        "XMPP_GUEST_DOMAIN": "guest.meet.lazymedia.media",
        "XMPP_MUC_DOMAIN": "muc.meet.lazymedia.media",
        "XMPP_RECORDER_DOMAIN": "recorder.meet.lazymedia.media"
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
        # Main domain (meet.lazymedia.media)
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
        
        # Auth domain (auth.meet.lazymedia.media)
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
        
        # Guest domain (guest.meet.lazymedia.media)
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
        
        # MUC domain (muc.meet.lazymedia.media)
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
        
        # Recorder domain (recorder.meet.lazymedia.media)
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