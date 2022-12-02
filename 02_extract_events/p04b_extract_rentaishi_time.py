import glob
from operator import is_
import os
import json
from value.bunsetsu import Bunsetsu
from value.event import Event
from typing import List, Tuple, Dict, Set,Optional
import csv

def extract_rentaishi_time(file:str):
    output_path=os.path.splitext(os.path.basename(file))[0]
    data={}
    with open(file,encoding="utf-8") as f:
        data=json.load(f)
    csv_output=[["text_id","text","time","person","act","time_parent"]]
    ouputs=[]
    for content in data["contents"]:
        for data in content["datas"]:
            for event in data["events"]:
                time_bnst=event["time"]["bnst_id"]
                if data["bunsetsu"][time_bnst]["is_rentaishi"]:
                    print("=====================================")
                    print("text_id:",data["text_id"])
                    out_text=""
                    for text in content["texts"]:
                        if text["text_id"]==data["text_id"]:
                            out_text=text["text"]
                            print(text["text"])
                    print("time:",data["bunsetsu"][time_bnst]["text"])
                    print("person:",event["person"]["text"])
                    print("act:","".join(event["act"]["texts"]))
                    ouputs.append({
                        "text":out_text,
                        "bunsetsu":data["bunsetsu"],
                        "event":event,
                    })
                    csv_output.append([
                        data["text_id"],
                        out_text,
                        data["bunsetsu"][time_bnst]["text"],
                        event["person"]["text"],
                        "".join(event["act"]["texts"]),
                        data["bunsetsu"][data["bunsetsu"][time_bnst]["parent"]]["text"]
                    ])
    with open(f"./p04b/{output_path}.json","w",encoding="utf-8") as f:
        json.dump({"contents":ouputs}, f, ensure_ascii=False, indent=2)
    with open(f"./p04b/{output_path}.csv","w",encoding="utf-8",newline="") as f:
        writer = csv.writer(f)
        for d in csv_output:
            writer.writerow(d)

os.makedirs("p04b", exist_ok=True)
files = glob.glob("./04/*.json")
for file in files:
    print(file)
    extract_rentaishi_time(file)