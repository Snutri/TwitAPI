import datetime
import json
time = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H%MZ")
def SendToFile(jsonfile):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(jsonfile, f, ensure_ascii=False, indent=4)
    return 1

def SendToTerminal(jsonfile):
    print(json.dumps(jsonfile, indent=4, sort_keys=True))
    return 1

def SendToArchive(jsonfile, searchterm, type):
    with open(f'{type}-{searchterm}-{time}.json', 'w', encoding='utf-8') as f:
        json.dump(jsonfile, f, ensure_ascii=False, indent=4)
    return 1