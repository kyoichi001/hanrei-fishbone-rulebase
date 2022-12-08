"""
マークされた時間表現の文節から、出来事の文節に当てはまるものを抽出
付随する文節をもとに、時間表現のタイプを決定する
"""

import glob
from operator import is_
import os
import json
import re
import csv
from value.time import Time
from typing import Optional

def export_to_json(filepath,data):
    with open(filepath, 'w', encoding='utf8', newline='') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    os.makedirs("02", exist_ok=True)
    files = glob.glob("./01/*.json")
    for file in files:
        print(file)
        output_path=os.path.splitext(os.path.basename(file))[0]
        index=0
        data={}
        with open(file,encoding="utf-8") as f:
            data=json.load(f)
            befTime=None
            for content in data["contents"]:
                for dat in content["datas"]:
                    events=[]
                    for bunsetsu in dat["bunsetsu"]:
                        t=extract_time(bunsetsu["text"],befTime)
                        if t is not None:
                            befTime=t
                            events.append({
                                "id":index,
                                "time":{
                                    "bnst_id":bunsetsu["id"],
                                    "text":bunsetsu["text"],
                                    "value":t.value()
                                }
                            })
                            index+=1
                    dat["events"]=events
                    #if len(events)!=0:
                    #    print(events)
                    index=0
        export_to_json(f"./02/{output_path}.json",data)

if __name__=="__main__":
    main()



