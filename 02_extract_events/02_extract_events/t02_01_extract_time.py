"""
マークされた時間表現の文節から、出来事の文節に当てはまるものを抽出
付随する文節をもとに、時間表現のタイプを決定する

時間の文節が一つの場合
{
    id:number//文節のID
    text:string
    value:number//日付を表す値
}

時間の文節が複数にまたがる場合
{
    bnst_ids:number[] //文節IDリスト
    span_text:{
        begin?:string //開始を表すテキスト
        end?:string //終了を表すテキスト
    }
    span_value:{
        begin?:number//開始となる日付
        end?:number//終了となる日付
    }
}


"""

import glob
from operator import is_
import os
import json
import re
import csv
from typing import Optional
from typing import List, Tuple, Dict, Set,Optional,Any

def extract_time(dat:Any):
    res=[]
    for bnst in dat["bunsetsu"]:
        if not bnst["is_rentaishi"] and bnst.get("time") is not None:
            res.append({
                "id":bnst["id"],
                "text":bnst["time"]["text"],
                "value":bnst["time"]["value"]
            })
    return res

def export_to_json(filepath,data):
    with open(filepath, 'w', encoding='utf8', newline='') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main(inputDir:str,outputDir:str):
    os.makedirs(outputDir, exist_ok=True)
    files = glob.glob(f"{inputDir}/*.json")
    for file in files:
        print(file)
        output_path=os.path.splitext(os.path.basename(file))[0]
        data={}
        with open(file,encoding="utf-8") as f:
            data=json.load(f)
            befTime=None
            index=0
            for content in data["contents"]:
                for dat in content["datas"]:
                    times=extract_time(dat)
                    if len(times)!=0:
                        dat["event"]={
                            "text_id":dat["text_id"],
                            "times":times
                        }
        export_to_json(f"{outputDir}/{output_path}.json",data)

if __name__=="__main__":
    main("../01_mark_data/03","01")



