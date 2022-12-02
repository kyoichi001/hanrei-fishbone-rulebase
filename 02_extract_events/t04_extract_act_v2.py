"""
行動の抽出
人物から文末、時間表現もしくは人物の文節までの動詞を抽出
そこから人物に関連した時間表現の文節を排除
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
            event["time"]["bnst_id"],
            event["time"]["text"],
            event["time"]["value"],
            event["person"]["bnst_id"],
            event["person"]["text"],
        )for event in text["events"]]
    time_bnsts=[event["time"]["bnst_id"] for event in text["events"]]
    person_bnsts=[event["person"]["bnst_id"] for event in text["events"]]

    for event in events:
        if event.person_id==-1:continue
        act_id=bnsts[event.person_id].parent_id
        event.act_ids=[]
        for bnst in range(event.time_id,len(bnsts)):
            bnst=bnst+1
            #print(bnst)
            if bnst in time_bnsts:
                if bnst!=event.time_id:break
                else:continue
            if bnst in person_bnsts:
                if bnst!=event.person_id:break
                else:continue
            event.act_ids.append(bnst-1)
        event.act_texts=[
            bnsts[id].text for id in event.act_ids
        ]
    return events

def main():
    os.makedirs("04", exist_ok=True)
    files = glob.glob("./03/*.json")
    for file in files:
        print(file)
        output_path=os.path.splitext(os.path.basename(file))[0]
        events=[]
        index=0
        data={}
        with open(file,encoding="utf-8") as f:
            data=json.load(f)
            befTime=None
            for content in data["contents"]:
                for dat in content["datas"]:
                    events=extract_from_text(dat)
                    dat["events"]=[
                        {
                            "id":event.id,
                            "time":{
                                "bnst_id":event.time_id,
                                "text":event.time_text,
                                "value":event.time_value
                            },
                            "person":{
                                "text":event.person_text,
                                "bnst_id":event.person_id
                            },
                            "act":{
                                "bnst_ids":event.act_ids,
                                "texts":event.act_texts
                            }
                        } for event in events
                    ]
        export_to_json(f"./04/{output_path}.json",data)
        
if __name__=="__main__":
    main()


