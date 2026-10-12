# edge_tts_compat.py

"""Point edge-tts speech synthesis at Microsoft's current endpoint.

The legacy host (speech.platform.bing.com/.../readaloud) started refusing
synthesis with HTTP 403, so a newer edge-tts does not help -- every released
version still hardcodes it. The voice-list REST API was *not* retired (it still
answers 200 on the legacy host and 403 on the new one), so only the synthesis
websocket is redirected here.
"""

import os

import edge_tts.communicate as _communicate
from dotenv import load_dotenv

# Current endpoint: Edge 155 synthesizes here, and it accepts the legacy
# trusted client token as the subscription key.
MSEDGE_WSS_URL = (
    "wss://api.msedgeservices.com/tts/cognitiveservices/websocket/v1"
    "?Ocp-Apim-Subscription-Key=6A5AA1D4EAFF4E9FB37E23D68491D6F4"
)


def _endpoint():
    # Env override is the rollback lever if Microsoft moves the endpoint again
    return os.getenv("EDGE_TTS_WSS_URL") or MSEDGE_WSS_URL


def install():
    """Redirect synthesis to the current endpoint. Safe to call repeatedly."""
    load_dotenv()
    _communicate.WSS_URL = _endpoint()
