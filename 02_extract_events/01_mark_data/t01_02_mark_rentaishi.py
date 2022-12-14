"""
連体詞かどうかのフラグの付与
TMSは～し、という文節を名詞・サ変可能としてしまうので、とりあえずは名詞に係っている文節のみを連体詞とする

現状、時間・人物の抽出は、パターンが含まれるかどうかで判別しているので、
連体詞を連結させても時間と人物を検出してしまう
なので、時間と人物を検出させた後に、その文節を無視するかを処理する
"""

import glob
from operator import is_
import os
import json
from re import T
from typing import List, Tuple, Dict, Set,Optional
from ..value.bunsetsu import Bunsetsu, Tango
from ..value.graph import Graph
from ..value.graph import Graph

def is_meishi(bunsetsu:Bunsetsu):
    for tango in bunsetsu.tangos:
        if tango.type1 in ["動詞","形容詞","副詞"]: return False
    return True

def export_to_json(filename:str,data)->None:
    with open(filename, 'w', encoding='utf8', newline='') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def check_rentaishi_(root:int,g:Graph,flagList:List[bool],bnsts:List[Bunsetsu]):
    children=g.g[root]
    for child in children:
        if flagList[root] or is_meishi(bnsts[root]):
            flagList[child]=True
        check_rentaishi_(child,g,flagList,bnsts)
        
def check_rentaishi(bnsts:List[Bunsetsu])->List[bool]:
    #print("check root")
    flagList=[False for i in range(len(bnsts))]
    flagList[bnsts[-1].id]=False
    li=[[] for i in range(len(bnsts)+1)]
    for bnst in bnsts:
        if bnst.parent_id!=-1:li[bnst.parent_id].append(bnst.id)
    g=Graph(li)
    check_rentaishi_(bnsts[-1].id,g,flagList,bnsts)
    for bnst in bnsts:
        bnst.is_rentaishi=flagList[bnst.id]
    return flagList

def main(inputDir:str,outputDir:str):
    os.makedirs(outputDir, exist_ok=True)
    files = glob.glob(f"{inputDir}/*.json")
    for file in files:
        print(file)
        data = open(file, "r", encoding="utf-8")
        data=json.load(data)
        for content in data["contents"]:
            for d in content["datas"]:
                bnsts:List[Bunsetsu]=[Bunsetsu(
                        bnst["id"],
                        bnst["to"],
                        [Tango(tango["content"],tango["type1"],tango["type2"],tango["type3"]) for tango in bnst["tangos"]]
                    ) for bnst in d["bunsetsu"]]
                b=check_rentaishi(bnsts)
                for bunsetsu in d["bunsetsu"]:
                    bunsetsu["is_rentaishi"]=b[bunsetsu["id"]]
        output_path=os.path.splitext(os.path.basename(file))[0]
        export_to_json(f"{outputDir}/{output_path}.json",data)

if __name__=="__main__":
    main("./01","./02")