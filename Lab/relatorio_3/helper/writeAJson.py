import json
import os
from bson import json_util # pip install bson

def writeAJson(data, name: str):
    parsed_json = json.loads(json_util.dumps(data))

    if not os.path.isdir("./relatório_3"):
        os.makedirs("./relatório_3")

    with open(f"./relatório_3/{name}.json", 'w', encoding='utf-8') as json_file:
        json.dump(parsed_json, json_file,
                  indent=4,
                  separators=(',', ': '),
                  ensure_ascii=False)