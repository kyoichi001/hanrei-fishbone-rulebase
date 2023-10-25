"""
行動の抽出
人物から文末、時間表現もしくは人物の文節までの動詞を抽出
そこから人物に関連した時間表現の文節を排除
"""

import csv
import glob
from operator import is_
import os
import json
from typing import List, Tuple, Dict, Set, Optional, Any,Union

def export_to_json(filepath, data):
    with open(filepath, 'w', encoding='utf8', newline='') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def extract_events_2(dat):
    """
    出来事の抽出
    eventとしての時間が抽出され（t02_01）、主語が検出されている場合のみ処理
    """
    def is_shugo(bst):
        if bst.get("is_rentaishi", False) or bst.get("person") is None:
            return False
        for tango in bst["tokens"]:
            if tango["text"] in ["は", "が", "も"] and "助詞" in tango["tag"].split("-"):
                return True
        return False
    def has_event_time(dat):
        if dat.get("event",{}).get("times") is None:return False
        return len(dat["event"]["times"])>0
    def get_event_time(dat,time_id):
        for time in dat["event"]["times"]:
            if time["event_time_id"]==time_id:return time
        return None
    def get_verb(bst):
        for tango in bst["tokens"]:
            if "動詞" in tango["tag"].split("-"):return bst["id"]
        return None
    if not has_event_time(dat): return [] 
    res = []
    extract_time = None
    acts: str = ""
    person = ""
    last_verb=None
    for bnst in dat["bunsetsu"]:
        # 時間か人物に係る文節なら行動として抽出しない
        if bnst.get("time_kakari", False) or bnst.get("person_kakari", False): continue
        if bnst.get("is_rentaishi", False):  # 連体詞であれば、人物か時間かの判定をせず、行動に追加
            acts += "".join([tango["text"] for tango in bnst["tokens"]])
            continue
        if bnst.get("event_time_id") is not None:
            time_obj=get_event_time(dat,bnst["event_time_id"])
            if time_obj is None:continue
            if extract_time is not None:  # すでにイベントを抽出していれば、抽出したイベントを出力に渡す
                res.append({
                    "person": person,
                    "time": extract_time,
                    "acts": acts
                })
                acts = ""
                person = ""
                last_verb=None
            extract_time = time_obj
            continue
        if bnst.get("person") is not None:  # 人物がくれば行動の抽出を終了
            if not is_shugo(bnst):  # 主語でない場合や主語の後動詞がないまま人物が来た場合スルー
                acts += "".join([tango["text"] for tango in bnst["tokens"]])
                continue
            if person != "":  # すでに人物を抽出していれば、抽出したイベントを出力に渡す
                res.append({
                    "person": person,
                    "time": extract_time,
                    "acts": acts
                })
                extract_time = None
                acts = ""
                last_verb=None
            person = bnst["person"]["content"]
            continue
        v=get_verb(bnst)
        if v is not None: last_verb=v
        acts += "".join([tango["text"] for tango in bnst["tokens"]])
    if extract_time is not None and person != "":  # すでにイベントを抽出していれば、抽出したイベントを出力に渡す
        res.append({
            "person": person,
            "time": extract_time,
            "acts": acts
        })
    return res

def export_to_csv(output_path, csv_datas):
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for d in csv_datas:
            writer.writerow(d)

def export_debug(data,outputDir:str,output_path:str)->None:
    import copy
    event_count=0
    csv_results:list[list[Union[int,str]]] = [["id",  "person", "begin_time","begin_value","end_time","end_value","point_time","point_value",  "act"]]
    index = 0
    for content in data["datas"]:
        if "events" not in content :continue
        for e in content["events"]:
            if e["person"] == "" or e["time"] == "" or e["time"] is None or e["acts"] == "":
                continue
            # print(e)
            csv_results.append([
                index,
                e["person"],
                e["time"].get("begin",{}).get("text"),
                e["time"].get("begin",{}).get("value"),
                e["time"].get("end",{}).get("text"),
                e["time"].get("end",{}).get("value"),
                e["time"].get("point",{}).get("text"),
                e["time"].get("point",{}).get("value"),
                e["acts"]
            ])
            index += 1
            c=copy.deepcopy(content)
            for kkk in c["bunsetsu"]:
                del kkk["tokens"]
            del c["event"]
            export_to_json(f"{outputDir}/events/{output_path}_{event_count}.json", c)
            event_count+=1
    export_to_csv(f"./p03/{output_path}.csv", csv_results)

def main(data):
    for content in data["datas"]:
        if content.get("event",{}).get("times") is None: continue
        ddd = extract_events_2(content)
        if len(ddd) != 0:
            content["events"] = ddd
    return data