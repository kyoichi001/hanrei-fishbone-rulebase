"""
時間表現に当てはまる文節のidから、その時間表現の主語を同定
"""

import glob
from operator import is_
import os
import json
from re import T
from value.sentence import Sentence
from value.bunsetsu import Bunsetsu
from value.event import Event
from typing import List, Tuple, Dict, Set,Optional
from value.graph import Graph
from rules.rule_loader import Rule,load_rules
from lib.dfs import DFS

def export_to_json(filename:str,data)->None:
    with open(filename, 'w', encoding='utf8', newline='') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def extract_person(bnsts:List[Bunsetsu],rules:List[Rule])->List[int]:
    """
    パターンに合うものを抽出
    """
    res=[]
    for bnst in bnsts:
        for rule in rules:
            if bnst.match_rule(rule):
                res.append(bnst.id-1)
    return res

def extract_from_text(rules,text):
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
            event["time"]["value"]
        )for event in text["events"]]
    sentence =Sentence(bnsts,events)
    sentence_graph=sentence.get_graph()
    person=extract_person(bnsts,rules)
    print(person)
    for event in events:
        lst=DFS(event.bnst-1,sentence_graph)
        min_val=10000000
        min_id=-1
        for p in person:
            j=bnsts[p].get_joshi()
            print(bnsts[p].mrph,j,lst[p])
            if j=="が" or j=="は":
                if min_val>lst[p]:
                    min_val=lst[p]
                    min_id=p
        if min_id!=-1:
            event.person_id=min_id
            event.person_text=bnsts[min_id].text
    return events


def main():
    os.makedirs("02", exist_ok=True)
    files = glob.glob("./01/*.json")
    rules=load_rules("./rules/rule_easy.json")
    for file in files:
        print(file)
        data = open(file, "r", encoding="utf-8")
        data=json.load(data)
        contents =data["contents"]
        for content in contents:
            if len(content["texts"])>0:
                print(content["texts"][0])
            for dat in content["datas"]:
                events=extract_from_text(rules,dat)
                dat["events"]=[
                    {
                        "id":event.id,
                        "bunsetsu":event.bnst,
                        "time":{
                            "text":event.time_text,
                            "value":event.time_value
                        },
                        "person":{
                            "text":event.person_text,
                            "bnst_id":event.person_id
                        }
                    } for event in events
                ]
        output_path=os.path.splitext(os.path.basename(file))[0]
        export_to_json(f"./02/{output_path}.json",data)

if __name__=="__main__":
    main()