import json


def save_session(packet_data, filename="session.json"):
    with open(filename, "w") as f:
        json.dump(packet_data, f, indent=4)


def load_session(filename="session.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except:
        return []