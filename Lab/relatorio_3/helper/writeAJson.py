import json
import os
from bson import json_util  # pip install bson


def writeAJson(data, name: str):
    parsed_json = json.loads(json_util.dumps(data))

    base_path = os.path.join("Lab", "relatorio_3", "json")

    os.makedirs(base_path, exist_ok=True)

    file_path = os.path.join(base_path, f"{name}.json")
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(parsed_json, json_file, indent=4, separators=(',', ': '))
