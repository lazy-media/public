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