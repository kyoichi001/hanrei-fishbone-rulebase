"""
時間表現に当てはまる文節のidから、その時間表現の主語を同定
"""

import glob
from operator import is_
import os
import json
from re import T
from typing import List, Tuple, Dict, Set,Optional

def export_to_json(filename:str,data)->None:
    with open(filename, 'w', encoding='utf8', newline='') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
def extract_main_people(dat):
    """
    文から主語を抜き取る
    bnstについて、personがNoneでなく、その助詞が「が」「は」「も」であり、is_rentaishiがfalse
    """
    res=[]
    for bnst in dat["bunsetsu"]:
        if not bnst["is_rentaishi"] and bnst.get("person") is not None:
            for tango in bnst["tangos"]:
                if tango["content"] in ["は","が","も"] and tango["type1"]=="助詞":
                    res.append({
                        "id":bnst["id"],
                        "person":bnst["person"]["content"],
                        "joshi":tango["content"]
                    })
                    break #単語の精査を終了し、次の文節へ
    return res


def main(inputDir:str,outputDir:str):
    os.makedirs(outputDir, exist_ok=True)
    files = glob.glob(f"{inputDir}/*.json")
    for file in files:
        print(file)
        data = open(file, "r", encoding="utf-8")
        data=json.load(data)
        contents =data["contents"]
        for content in contents:
            #if len(content["texts"])>0:
            #    print(content["texts"][0])
            for dat in content["datas"]:
                people=extract_main_people(dat)
                if len(people)!=0:
                    if dat.get("event") is not None:
                        dat["event"]["people"]=people
                    else:
                        dat["event"]={
                            "people":people
                        }
        output_path=os.path.splitext(os.path.basename(file))[0]
        export_to_json(f"{outputDir}/{output_path}.json",data)

if __name__=="__main__":
    main("./01","./02")