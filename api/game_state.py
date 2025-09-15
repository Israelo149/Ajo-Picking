import json

def handler(request):
    state = {
        "tiles": [{"id": i, "number": i+1, "pickedBy": None} for i in range(20)],
        "picksMade": 0,
        "revealed": False,
        "selections": []
    }
    return {
        "statusCode": 200,
        "headers": { "Content-Type": "application/json" },
        "body": json.dumps(state)
    }
