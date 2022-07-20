from binascii import b2a_qp
import datetime
import os
import json
import pandas as pd
time = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H%MZ")
def SendToFile(jsonfile, searchterm, type):
    with open(f'{type}-{searchterm}-{time}.json', 'w', encoding='utf-8') as f:
        json.dump(jsonfile, f, ensure_ascii=False, indent=4)
    return 1

def SendToTerminal(jsonfile):
    print(json.dumps(jsonfile, indent=4, sort_keys=True))
    return 1

def SendToArchive(jsonfile, searchterm, user):
    filename=f'{user}-{searchterm}.json'

    if (os.path.exists(filename) and (os.path.getsize(filename)>0)):
        
        with open(filename,'r+') as file:

            a = json.load(file)
            a2 = json.dumps(a)
            b3 = json.dumps(jsonfile)

            jsonMerged = {**json.loads(a2), **json.loads(b3)}

            json.dump(jsonMerged, file, indent=4)



        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(jsonMerged, f, ensure_ascii=False, indent=4)
    else:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(jsonfile, f, ensure_ascii=False, indent=4)
 
    return 1

#comments of shame on appending to file

            #purely adds second dicts values after the existing one
                    #c = dict(list(a.data.items()) + list(jsonfile.data.items()))

            #produces new dict after the existing ones
                    #d = Merge(a,b2)

            #seemingly doesnt work, produces null after existing one
                    #e = b2.update(a)

            #seemingly doesnt work, produces one string line after the existing one
                    #g = {**a, **b2}

            #method h, also didnt work, had trouble with it thinking the values being dict
                    #df1 = pd.read_json(a, lines=True)
                    #df2 = pd.read_json(jsonfile, lines=True)
                    #       
                    #df = df1.merge(df2, on='id')
                    #print(df)

            #method i, again a failure, coulnt pinpoint data attribute
                    #dictA = a
                    #dictB = jsonfile
                    #
                    #merged_dict = {key: value for (key, value) in (dictA.data() + dictB.data())}
                    #
                    ## string dump of the merged dict
                    #jsonString_merged = json.dumps(merged_dict)
                    #print(jsonString_merged)
