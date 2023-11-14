import json

def loadConfig(path):
    with open(path,"r") as f:
        load_dict = json.load(f)
    return load_dict