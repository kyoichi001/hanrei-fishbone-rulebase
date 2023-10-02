"""
動詞について、動作主が誰かマークする
"""

import csv
import glob
from operator import is_
import os
import json
from typing import List, Tuple, Dict, Set, Optional, Any,Union

def mark_verb(dat):
    def is_shugo(bst):
        if bst.get("is_rentaishi", False) or bst.get("person") is None:
            return False
        for tango in bst["tokens"]:
            if tango["text"] in ["は", "が", "も"] and "助詞" in tango["tag"].split("-"):
                return True
        return False
    def get_verb(bst):
        for tango in bst["tokens"]:
            if "動詞" in tango["tag"].split("-"):return bst["id"]
        return None
    person=None
    for bnst in dat["bunsetsu"]:
        if bnst.get("is_rentaishi", False): continue
        if get_verb(bnst)and person is not None:
            bnst["verb_person"]=person
        if bnst.get("person") is not None:  # 人物がくれば行動の抽出を終了
            if not is_shugo(bnst):continue
            print(bnst["person"])
            person={
                "id":bnst["id"],
                "str":bnst["person"]["content"]
            }

def export_to_json(filename: str, data) -> None:
    with open(filename, 'w', encoding='utf8', newline='') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def export_to_csv(output_path, csv_datas):
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for d in csv_datas:
            writer.writerow(d)

def export_debug(data,outputDir,output_path):
    import copy
    os.makedirs(outputDir+"/debug", exist_ok=True)
    count=0
    def has_verb(bnsts):
        for bnst in bnsts:
            if "verb_person" in bnst:return True
        return False
    for content in data["datas"]:
        c=copy.deepcopy(content)
        if not has_verb(c["bunsetsu"]):continue
        for bnst in c["bunsetsu"]:
            del bnst["tokens"]
            if "times" in bnst:del bnst["times"]
        if "event"in c:del c["event"]
        export_to_json(f"{outputDir}/debug/{output_path}_{count}.json", c)
        count+=1
    

def main(inputDir: str, outputDir: str):
    os.makedirs(outputDir, exist_ok=True)
    files = glob.glob(f"{inputDir}/*.json")
    for file in files:
        print(file)
        filedat = open(file, "r", encoding="utf-8")
        data = json.load(filedat)
        for content in data["datas"]:
            mark_verb(content)
        output_path = os.path.splitext(os.path.basename(file))[0]
        export_debug(data,outputDir,output_path)
        export_to_json(f"{outputDir}/{output_path}.json", data)

if __name__ == "__main__":
    main("./03", "./04")