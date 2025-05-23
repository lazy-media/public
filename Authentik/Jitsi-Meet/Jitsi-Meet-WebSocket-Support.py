# Ensure WebSocket (wss://) and BOSH (http-bind) are allowed
if request.path.startswith("/xmpp-websocket") or request.path.startswith("/http-bind"):
    return True  # Allow WebSocket/XMPP traffic
else:
    return request.host == "meet.YOUR.DOMAIN"  # Only allow Jitsi domain