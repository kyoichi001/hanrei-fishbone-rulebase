"""
名詞・接頭詞しかない文節同士（＋隣同士の文節で、かつ直接係っている）を連結させ、一つの文節に加工する
"""

import glob
from operator import is_
import os
import json
from re import T
import csv
from typing import List, Tuple, Dict, Set, Any

def is_meishi(bst):
    """
    文節の中にある単語が名詞・接頭詞のみか
    """
    for tango in bst["tangos"]:
        if not ((tango["type1"]=="名詞" or tango["type1"]=="接頭詞")and tango["type2"]!="非自立" ):
            return False
    return True

def merge_tree(bsts:List[Any],bst1:int,bst2:int):
    """
    bsts[bst1]をbsts[bst2]に結合する
    """
    #print(bsts[bst1])
    tangos=[]
    tangos.extend(bsts[bst1]["tangos"])
    tangos.extend(bsts[bst2]["tangos"])
    bsts[bst1]={
        "id":bsts[bst1]["id"],
        "to":bsts[bst2]["to"],
        "tangos":tangos
    }
    #print(bsts[bst1])
    for bst in bsts:
        if bst["id"]>bsts[bst1]["id"]:bst["id"]-=1
        if bst["to"]>bsts[bst1]["id"]:bst["to"]-=1
    del bsts[bst2]
    return bsts

def conbine_bunsetsu(bsts):
    #print("start conbining...")
    conbine_to_next=[False for i in range(len(bsts))]
    for i in range(len(bsts)-1):
        if is_meishi(bsts[i]) and bsts[i]["to"]==bsts[i+1]["id"]:
            conbine_to_next[i]=True
    index=len(bsts)-1
    while True:
        if index<0:break
        #print("len bef",len(bsts))
        if conbine_to_next[index-1]:
            bsts=merge_tree(bsts,index-1,index)
            del conbine_to_next[index-1]
        index-=1
        #print("len aft",len(bsts))
    return bsts

def export_to_json(filepath,data):
    with open(filepath, 'w', encoding='utf8', newline='') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main(inputDir:str,outputDir:str):
    os.makedirs(outputDir, exist_ok=True)
    json_files = glob.glob(f"{inputDir}/*.json")
    for file in json_files:
        print(file)
        data={}
        with open(file,encoding="utf-8") as f:
            data=json.load(f)
            for content in data["contents"]:
                for dat in content["datas"]:
                    newBsts=conbine_bunsetsu(dat["bunsetsu"])
                    dat["bunsetsu"]=newBsts
        output_path=os.path.splitext(os.path.basename(file))[0]
        export_to_json(f"{outputDir}/{output_path}.json",data)

if __name__=="__main__":
    main("./fishbone_out","./02")