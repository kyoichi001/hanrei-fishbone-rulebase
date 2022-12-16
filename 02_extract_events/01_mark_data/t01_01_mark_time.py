"""
KNPの結果から、時間表現に当てはまる文節のidのリストを出力
"""

import glob
from operator import is_
import os
import json
import re
import csv
from value.time import Time
from typing import Optional
from typing import List, Tuple, Dict, Set, Any

def extract_time_(rule,s:str,befTime:Time)->Tuple[Time,str]|None:
    regex=rule["regex"]
    same=rule.get("same")
    res=Time()
    a= re.search(regex,s)
    if a is None: return None
    gengo_str=a.groupdict().get("gengo")
    year_str=a.groupdict().get("year")
    month_str=a.groupdict().get("month")
    day_str=a.groupdict().get("day")
    if gengo_str is not None:
        if gengo_str=="昭和":res.year+=1925
        elif gengo_str=="平成":res.year+=1988
        elif gengo_str=="令和":res.year+=2018
    if year_str is not None:
        if year_str=="元":
            res.year+=1
        else:
            res.year+=int(year_str)
    if month_str is not None:
        res.month=int(month_str)
    if day_str is not None:
        res.day=int(day_str)
    if same is not None:
        if same=="year":res.year=befTime.year
        elif same=="month":res.month=befTime.month
        elif same=="day":res.day=befTime.day
    return res, a.group()

def export_to_json(filepath,data):
    with open(filepath, 'w', encoding='utf8', newline='') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def export_to_csv(filepath,data):
    import csv
    with open(filepath, 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        for row in data:
            writer.writerow(row)


def extract_time(rules,tangos:List[Any],befTime:Time)->Optional[Tuple[Time,str]]:
    for rule in rules:
        for tango in tangos:
            obj=extract_time_(rule,tango["content"],befTime)
            if obj is not None:
                return obj[0],obj[1]
    return None
    
def main(inputDir:str,outputDir:str):
    os.makedirs(outputDir, exist_ok=True)
    files = glob.glob(f"{inputDir}/*.json")
    csv_res=[["id","text_id","bunsetsu","text","value"]]
    count=0
    rules_data=[]
    with open("./rules/time_rules.json",encoding="utf-8") as f:
        rules_data=json.load(f)["point"]
    for file in files:
        print(file)
        data={}
        with open(file,encoding="utf-8") as f:
            data=json.load(f)
            befTime=None
            for content in data["contents"]:
                for dat in content["datas"]:
                    for bunsetsu in dat["bunsetsu"]:
                        t=extract_time(rules_data,bunsetsu["tangos"],befTime)
                        if t is not None:
                            befTime=t[0]
                            bunsetsu["time"]={
                                "text":t[1],
                                "value":t[0].value()
                            }
                            csv_res.append([count,dat["text_id"],"".join([tango["content"] for tango in bunsetsu["tangos"]]),t[1],t[0].value()])
                            count+=1
        output_path=os.path.splitext(os.path.basename(file))[0]
        export_to_json(f"{outputDir}/{output_path}.json",data)
    export_to_csv(f"{outputDir}/time_list.csv",csv_res)

if __name__=="__main__":
    main("../00_process_data/03","./01")



