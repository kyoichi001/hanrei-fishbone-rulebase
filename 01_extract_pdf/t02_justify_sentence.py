"""

セルをx,y座標で並び替える
y座標が同じなら結合

"""

import csv
from typing import List, Tuple, Dict, Set,Optional
import re
import json

def export_to_json(filename:str,data)->None:
    obj={
        "header":{# TODO:
            "texts_count":len(data)
        },
        "contents":data
    }
    with open(filename, 'w', encoding='utf8', newline='') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def clean_text(txt:str)->str:
    return txt.strip().replace('\n', '').replace('\t', '').replace("（","(").replace("）",")")

def main_func(data):
    res = sorted(data["contents"],key=lambda x: (-x["y"],x["x"]))
    if len(res)==1:
        return [clean_text(i["text"]) for i in res if clean_text(i["text"])!="" and re.match('^[-ー \d]+$', i["text"]) == None]
    
    i=1
    while i<len(res):#同じy座標にあるテキストを結合（行番号(5,10,15,...)と本文の座標が同じだとエラー)
        if res[i-1]["y"]==res[i]["y"]:
            #print("!!!!!!!!!!!!",res[i-1]["text"],res[i]["text"])
            res[i-1]["text"]+=res[i]["text"]
            res.pop(i)
            continue
        i+=1

    return [clean_text(i["text"]) for i in res if clean_text(i["text"])!="" and re.match('^[-ー \d]+$', i["text"]) == None]

            
import glob
import os

def main():
    os.makedirs("02", exist_ok=True)
    files = glob.glob("./01/*.json")

    for file in files:
        print(file)
        contents = open(file, "r", encoding="utf-8")
        pages=json.load(contents)["pages"]
        #print(f"入力 {len(contents)}行")
        output=[]
        for page in pages:
            output.extend(main_func(page))
        output_path=os.path.splitext(os.path.basename(file))[0]
        #print(f"出力 {len(container)}行")
        export_to_json(f"./02/{output_path}.json",output)

if __name__=="__main__":
    main()