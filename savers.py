from binascii import b2a_qp
import datetime
import os
import json
import pandas as pd
import jsonmerge
import requests
import sys
import shutil
c_timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d-%H%MZ")
def SendToFile(jsonfile, searchterm, type):
    with open(f'{type}-{searchterm}-{c_timestamp}.json', 'w', encoding='utf-8') as f:
        json.dump(jsonfile, f, ensure_ascii=False, indent=4)
    return 1

def SendToTerminal(jsonfile):
    print(json.dumps(jsonfile, indent=4, sort_keys=True))
    return 1

def SendToArchive(jsonfile, searchterm, user):
    filename=f'{user}-{searchterm}.json'

    if (os.path.exists(filename) and (os.path.getsize(filename)>0)):

        with open(filename,'r+', encoding='utf-8') as file:
        
            a = json.load(file)
            schema = {
                "properties": {
                  "data": {
                    "mergeStrategy": "arrayMergeById"
                }, 
                "includes": {
                    "type": "object",
                    "properties": {
                      "users": {
                        "mergeStrategy": "arrayMergeById"
                      },
                      "tweets": {
                        "mergeStrategy": "arrayMergeById"
                      },
                      "polls": {
                        "mergeStrategy": "arrayMergeById"
                      },
                      "places": {
                        "mergeStrategy": "arrayMergeById"
                      },
                      "media": {
                        "mergeStrategy": "append"
                      }
                    }
                  }
                }
            }
            merger = jsonmerge.Merger(schema)
            base = a
            base = merger.merge(base, jsonfile)

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(base, f, ensure_ascii=False, indent=4)
    else:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(jsonfile, f, ensure_ascii=False, indent=4)
 
    return 1

def SendToImages(path, image, key):
    if not image:
        return
    ext = os.path.splitext(image)[1]
    name = key + ext
    save_dest = os.path.join(path, name)
    if not os.path.exists(save_dest):
        size = "large"
        r = requests.get(image + ":" + size, stream=True)
        if r.status_code == 200:
            with open(save_dest, "wb") as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
            print(f"{name} saved")
    else:
        print(f"Skipping {name}: already downloaded")
