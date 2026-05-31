import json

def load_features():
    with open("features.json", "r") as f:
        return json.load(f)

def save_features(data):
    with open("features.json", "w") as f:
        json.dump(data, f, indent=4)

def enable_feature(name):
    data = load_features()
    data[name] = True
    save_features(data)

def disable_feature(name):
    data = load_features()
    data[name] = False
    save_features(data)
