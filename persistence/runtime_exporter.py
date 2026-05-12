import json

def export_runtime_json(fsm, path):
    data = fsm.to_dict()

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)