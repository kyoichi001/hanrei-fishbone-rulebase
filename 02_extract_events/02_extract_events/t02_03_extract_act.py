"""
行動の抽出
人物から文末、時間表現もしくは人物の文節までの動詞を抽出
そこから人物に関連した時間表現の文節を排除
"""

"""

"event": {
    "text_id": 22,
    "times": [
        {
            "id": 1,
            "text": "平成２８年４月２６日",
            "value": 20160426
        }
    ],
    "people": [
        {
            "id": 0,
            "person": "被告",
            "joshi": "は"
        }
    ]
}
"""

import glob
from operator import is_
import os
import json
from typing import List, Tuple, Dict, Set,Optional,Any

def export_to_json(filepath,data):
    with open(filepath, 'w', encoding='utf8', newline='') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def extract_events(dat):
    res=[]
    for bnst in dat["bunsetsu"]:
        if bnst["is_rentaishi"] :continue
        for tango in bnst["tangos"]:
            if tango["type1"]=="動詞":
                res.append({
                    "id":bnst["id"],
                    "tangos":"".join([tango["content"] for tango in bnst["tangos"]])
                })
                break #単語の精査を終了し、次の文節へ
    return res

def main(inputDir:str,outputDir:str):
    os.makedirs(outputDir, exist_ok=True)
    files = glob.glob(f"{inputDir}/*.json")
    for file in files:
        print(file)
        output_path=os.path.splitext(os.path.basename(file))[0]
        index=0
        data={}
        with open(file,encoding="utf-8") as f:
            data=json.load(f)
            for content in data["contents"]:
                for dat in content["datas"]:
                    if dat.get("event") is None:continue
                    if dat["event"].get("people") is None:continue
                    #if dat["event"].get("times") is None:continue
                    dat["event"]["acts"]=extract_events(dat)
        export_to_json(f"{outputDir}/{output_path}.json",data)
        
if __name__=="__main__":
    main("./02","./03")


