
import glob
from operator import is_
import os
import json
from value.bunsetsu import Bunsetsu
from value.event import Event
from typing import List, Tuple, Dict, Set,Optional


def to_txt(file:str):
    output_path=os.path.splitext(os.path.basename(file))[0]
    data={}
    with open(file,encoding="utf-8") as f:
        data=json.load(f)
    with open(f"./p03/{output_path}.txt","w",encoding="utf-8") as f:
        for content in data["contents"]:
            event_count=0
            for text in content["datas"]["texts"]:
                event_count+=len(text["events"])
            if event_count==0:continue
            f.write("=========================================================\n")
            for text in content["texts"]:
                f.write(text)
                f.write("\n")
            for text in content["datas"]["texts"]:
                for event in text["events"]:
                    f.write("time ========\n")
                    f.write(event["time"]["text"])
                    f.write("\n")
                    f.write("person ======\n")
                    f.write(f'{event["person"]["text"]}, {event["person"]["bnst_id"]}')
                    f.write("\n")
                    f.write("act =========\n")
                    f.write("".join(event["act"]["texts"]))
                    f.write("\n")
            f.write("=========================================================\n")
            f.write("\n")
import csv
def to_csv(file:str):
    output_path=os.path.splitext(os.path.basename(file))[0]
    data={}
    with open(file,encoding="utf-8") as f:
        data=json.load(f)
    res=[["id","text","person","point","point_value","begin","begin_value","end","end_value","act"]]
    id=0
    for content in data["datas"]:
        if "events" not in content:continue
        for event in content["events"]:
            #if "time" not in event or event.get("time") is None:continue
            time=event.get("time")
            if time is None:time={}
            #if "person" not in event or event.get("person") is None or event["person"]=="":continue
            print(type(event),event["time"])
            d=[
                id,
                content["text"],#TODO text_idに合わせてテキスト本文を取得（text, selif, blacketsそれぞれ対応）
                event["person"],
                time.get("point",{}).get("text",None),
                time.get("point",{}).get("value",None),
                time.get("begin",{}).get("text",None),
                time.get("begin",{}).get("value",None),
                time.get("end",{}).get("text",None),
                time.get("end",{}).get("value",None),
                event["acts"],
            ]
            res.append(d)
            id+=1
    with open(f"./p03/{output_path}.csv","w",encoding="utf-8",newline="") as f:
        writer = csv.writer(f)
        for d in res:
            writer.writerow(d)
            
os.makedirs("p03", exist_ok=True)
files = glob.glob("./05/*.json")
for file in files:
    print(file)
    to_csv(file)