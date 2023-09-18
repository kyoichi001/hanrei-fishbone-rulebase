"""
マークされた時間表現の文節から、出来事の文節に当てはまるものを抽出
文節のリストを入力とし、時間オブジェクト（以下参照）のリストを出力する

```
{
    bnst_ids:number[] //文節IDリスト
    span_text:{
        begin?:string //開始を表すテキスト
        end?:string //終了を表すテキスト
        point?:string//一点を表すテキスト
    }
    span_value:{
        begin?:number //開始となる日付
        end?:number //終了となる日付
        point?:number //一点の時間の日付
    }
}
```
## 疑似コード
1. for bnst in bnsts
    1. if bnst has times and bnst is not rentaishi
        1. let queue; queue.push(bnst)
    1. while len(queue)!=0:
        1. bnst= queue.top; queue.pop
        1. for time in bnst.times
            1. time_typeがmodのときは、bnst_idsに文節IDを加えるだけでなにもしない
            1. time_typeがbegin,endのときも同様
            1. time_typeがpointのときは、span_text.point, span_value.pointにそれぞれ値を格納
            1. 一つの文節にbegin,endが同時に含まれる場合は一番後ろの単語を優先
        1. if bnst.before has times
            1. queue.push(bnst)
    1. 得られた時間オブジェクトを出力にpush。再度文節リストを精査（連続する時間表現を除く）
"""

import glob
from operator import is_
import os
import json
import re
import csv
from typing import Optional
from typing import List, Tuple, Dict, Set, Optional, Any
from collections import deque

def bnst2time(bnst):
    res={
        "bnst_ids":[bnst["id"]]
    }
    mode="point"
    for time in reversed(bnst["times"]): #その文節に含まれる時間表現（「～日」「～まで」など）をすべて一つのイベントにまとめる
        if time["type"] == "point":
            if mode=="point" and "point" not in res:res[mode]={"text":"","value":0}
            res[mode]["text"] = time["text"]+res[mode]["text"]
            res[mode]["value"] = time["value"]
            mode = "point"
        elif time["type"] == "begin" and mode == "point": #「～から」という語句が含まれる場合、後に現れる時間をbegin_timeにする
            mode = "begin"
            res[mode]={"text":time["text"],"value":0}
        elif time["type"] == "end" and mode == "point":
            mode = "end"
            res[mode]={"text":time["text"],"value":0}
        elif time["type"] == "other":
            pass
    return res

def timegroup2time(bnsts,bnst_ids):
    res={
        "bnst_ids":bnst_ids
    }
    for bnst in bnsts:
        if bnst["id"] not in bnst_ids:continue
        time_obj=bnst2time(bnst)
        if "begin" in time_obj:
            res["begin"]=time_obj["begin"]
        elif "end" in time_obj:
            res["end"]=time_obj["end"]
        elif "point" in time_obj:
            res["point"]=time_obj["point"]
    return res

def extract_time(dat: Any):
    res = []
    i = len(dat["bunsetsu"])-1
    visited=[False for i in range(len(dat["bunsetsu"]))]
    while i >= 0:  # 文節を後ろから見る
        bnst = dat["bunsetsu"][i]
        if visited[i]:
            i-=1
            continue
        if not bnst.get("is_rentaishi", False) and bnst.get("times") is not None:
            # 連体詞でないかつtimesプロパティを持つなら、出力の文節idリストに追加し、抽出フラグを立てる
            if "time_group" in bnst:
                time_obj=timegroup2time(dat["bunsetsu"],bnst["time_group"])
                for j in bnst["time_group"]:visited[j]=True
                res.append(time_obj)
            else:
                time_obj=bnst2time(bnst)
                res.append(time_obj)
        visited[i]=True
        i -= 1
    return list(reversed(res))


def export_to_json(filepath, data):
    with open(filepath, 'w', encoding='utf8', newline='') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main(inputDir: str, outputDir: str):
    os.makedirs(outputDir, exist_ok=True)
    files = glob.glob(f"{inputDir}/*.json")
    for file in files:
        print(file)
        output_path = os.path.splitext(os.path.basename(file))[0]
        f = open(file, "r", encoding="utf-8")
        data = json.load(f)
        for content in data["datas"]:
            times = extract_time(content)
            if len(times) != 0:
                content["event"] = {
                    "text_id": content["text_id"],
                    "times": times
                }
        export_to_json(f"{outputDir}/{output_path}.json", data)


if __name__ == "__main__":
    main("../01_mark_data/04", "01")
