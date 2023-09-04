"""
時間表現に当てはまる文節のidから、その時間表現の主語を同定
"""

import glob
from operator import is_
import os
import json
import re
from re import T
from typing import List, Tuple, Dict, Set,Optional
from value.bunsetsu import Bunsetsu,Tango,Sentence
from value.event import Event
from value.graph import Graph
from rules.rule_loader import Rule,load_rules

def match_rule(tango:Tango,rule:Rule)->bool:
    if rule.types=="c": return tango.content==rule.content #テキストを直接指定
    if rule.types=="type":
        tgs=tango.tags.split("-")
        return rule.content in tgs #品詞
    if rule.types=="regex": return re.fullmatch(rule.content,tango.content) is not None #正規表現
    return True

def export_to_json(filename:str,data)->None:
    with open(filename, 'w', encoding='utf8', newline='') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def mark_person(rules,bunsetsu):
    bnst=Bunsetsu(
            bunsetsu["id"],
            bunsetsu["to"],
            [Tango(tango["text"],tango["tag"]) for tango in bunsetsu["tokens"]]
        )
    flg=False
    content=""
    for tango in bnst.tangos:
        tgs=tango.tags.split("-")
        #if "名詞" not in tgs and  "助詞" not in tgs:return bunsetsu
        #if "名詞" in tgs and "読点" not in tgs:content=tango.content
        #if "助詞" in tgs:
        #    flg = tango.content in ["は", "が", "も"]
        #    if not flg:return bunsetsu #それ以外の助詞が入っていたら排除
        #if content!="" and flg:break
        for rule in rules:
            if match_rule(tango,rule):
                bunsetsu["person"]={
                    "content":tango.content,
                }
                return bunsetsu
    if flg:
        bunsetsu["person"]={
            "content":content,
        }
    return bunsetsu


def main(inputDir:str,outputDir:str):
    os.makedirs(outputDir, exist_ok=True)
    files = glob.glob(f"{inputDir}/*.json")
    rules=load_rules("./rules/rule.json")
    for file in files:
        print(file)
        filedat = open(file, "r", encoding="utf-8")
        data=json.load(filedat)
        contents =data["datas"]
        for content in contents:
            if "texts" not in content:continue
            #if len(content["texts"])>0:
            #    print(content["texts"][0])
            for bunsetsu in content["bunsetsu"]:
                bunsetsu=mark_person(rules,bunsetsu)
        output_path=os.path.splitext(os.path.basename(file))[0]
        export_to_json(f"{outputDir}/{output_path}.json",data)

if __name__=="__main__":
    main("./02","./03")