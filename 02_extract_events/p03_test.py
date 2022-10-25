
import glob
from operator import is_
import os
import json
from value.bunsetsu import Bunsetsu
from value.event import Event
from typing import List, Tuple, Dict, Set,Optional

os.makedirs("p03", exist_ok=True)
files = glob.glob("./03/*.json")

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
    res=[["id","text","person","time","time_value","act"]]
    id=0
    for content in data["contents"]:
        id2text={}
        for text in content["texts"]:
            id2text[text["text_id"]]=text["text"]
        for selif in content["selifs"]:
            id2text[selif["text_id"]]=selif["content"]
        for blacket in content["blackets"]:
            id2text[blacket["text_id"]]=blacket["content"]
        for dat in content["datas"]:
            for event in dat["events"]:
                d=[
                    id,
                    id2text[dat["text_id"]],#TODO text_idに合わせてテキスト本文を取得（text, selif, blacketsそれぞれ対応）
                    event["person"]["text"],
                    event["time"]["text"],
                    event["time"]["value"],
                    "".join(event["act"]["texts"]),
                ]
                res.append(d)
                id+=1
    with open(f"./p03/{output_path}.csv","w",encoding="utf-8",newline="") as f:
        writer = csv.writer(f)
        for d in res:
            writer.writerow(d)
for file in files:
    print(file)
    to_csv(file)