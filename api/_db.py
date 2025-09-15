import os
import json
import redis

url = (
    os.environ.get("KV_URL") or
    os.environ.get("REDIS_URL") or
    os.environ.get("UPSTASH_REDIS_URL") or
    os.environ.get("VERCEL_KV_URL")
)

if not url:
    raise RuntimeError("❌ Redis URL not found in environment variables!")

r = redis.from_url(url)

DEFAULT_STATE = {
    "tiles": [{"id": i, "number": i+1, "pickedBy": None} for i in range(20)],
    "picksMade": 0,
    "revealed": False,
    "selections": []
}

def get_state():
    state = r.get("game_state")
    if state:
        return json.loads(state)
    return DEFAULT_STATE

def save_state(state):
    r.set("game_state", json.dumps(state))
