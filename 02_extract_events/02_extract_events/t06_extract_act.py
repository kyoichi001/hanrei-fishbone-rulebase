"""
行動の抽出
人物の文節に係る動詞を特定し、人物からその動詞までの文節を行動として抽出（改善が必要なら適宜修正）
"""
import glob
from operator import is_
import os
import json
from value.bunsetsu import Bunsetsu
from value.event import Event
from typing import List, Tuple, Dict, Set,Optional

def export_to_json(filepath,data):
    with open(filepath, 'w', encoding='utf8', newline='') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def extract_from_text(text):
    bnsts:List[Bunsetsu]=[Bunsetsu(
            bnst["id"],
            bnst["text"],
            bnst["mrph"],
            bnst["parent"],
            bnst["type"],
            bnst["type2"]
        ) for bnst in text["bunsetsu"]]
    events:List[Event]=[Event(
            event["id"],
            event["bunsetsu"],
            event["time"]["text"],
            event["time"]["value"],
            event["person"]["bnst_id"],
            event["person"]["text"],
        )for event in text["events"]]
    for event in events:
        if event.person_id==-1:continue
        act_id=bnsts[event.person_id].parent_id
        event.act_ids=[
            id for id in range(event.person_id,act_id) if id != event.person_id and id != event.time_id-1
        ]
        
        event.act_texts=[
            bnsts[id].text for id in event.act_ids
        ]
    return events

def main():
    os.makedirs("03", exist_ok=True)
    files = glob.glob("./02/*.json")
    for file in files:
        print(file)
        output_path=os.path.splitext(os.path.basename(file))[0]
        events=[]
        data={}
        with open(file,encoding="utf-8") as f:
            data=json.load(f)
            for content in data["contents"]:
                for dat in content["datas"]:
                    events=extract_from_text(dat)
                    dat["events"]=[
                        {
                            "id":event.id,
                            "bunsetsu":event.time_id,
                            "time":{
                                "text":event.time_text,
                                "value":event.time_value
                            },
                            "person":{
                                "text":event.person_text,
                                "bnst_id":event.person_id
                            },
                            "act":{
                                "ids":event.act_ids,
                                "texts":event.act_texts
                            }
                        } for event in events
                    ]
        export_to_json(f"./03/{output_path}.json",data)
        
if __name__=="__main__":
    main()


