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

def bnst2time(bnst,event_time_id):
    res={
        "event_time_id":event_time_id,
        "bnst_ids":[bnst["id"]]
    }
    bnst["event_time_id"]=event_time_id
    mode="point"
    has_value=False
    for time in reversed(bnst["times"]): #その文節に含まれる時間表現（「～日」「～まで」など）をすべて一つのイベントにまとめる
        if time["type"] == "point":
            if mode=="point" and "point" not in res:res[mode]={"text":"","value":0}
            res[mode]["text"] = time["text"]+res[mode]["text"]
            res[mode]["value"] = time["value"]
            has_value=True
            mode = "point"
        elif time["type"] == "begin" and mode == "point": #「～から」という語句が含まれる場合、後に現れる時間をbegin_timeにする
            mode = "begin"
            res[mode]={"text":time["text"],"value":0}
        elif time["type"] == "end" and mode == "point":
            mode = "end"
            res[mode]={"text":time["text"],"value":0}
        elif time["type"] == "other":
            pass
    return res,has_value

def timegroup2time(bnsts,bnst_ids,event_time_id):
    res={
        "event_time_id":event_time_id,
        "bnst_ids":bnst_ids
    }
    has_value=False
    for bnst in bnsts:
        if bnst["id"] not in bnst_ids:continue
        time_obj,has_value_=bnst2time(bnst,event_time_id)
        bnst["event_time_id"]=event_time_id
        if has_value_:has_value=True
        else:continue
        if "begin" in time_obj:
            res["begin"]=time_obj["begin"]
        elif "end" in time_obj:
            res["end"]=time_obj["end"]
        elif "point" in time_obj:
            res["point"]=time_obj["point"]
        #if has_value_:has_value=True
    return res,has_value

def extract_time(dat: Any,event_time_id):
    res = []
    i = len(dat["bunsetsu"])-1
    visited=[False for i in range(len(dat["bunsetsu"]))]
    while i >= 0:  # 文節を後ろから見る
        bnst = dat["bunsetsu"][i]
        if visited[i]:
            i-=1
            continue
        if not bnst.get("is_rentaishi", False) and bnst.get("times") is not None:
            # 連体詞でないかつtimesプロパティを持つなら
            if "time_group" in bnst:
                time_obj,has_value=timegroup2time(dat["bunsetsu"],bnst["time_group"],event_time_id)
                for j in bnst["time_group"]:visited[j]=True
                if has_value:
                    res.append(time_obj)
                    event_time_id+=1
            else:
                time_obj,has_value=bnst2time(bnst,event_time_id)
                if has_value:
                    res.append(time_obj)
                    event_time_id+=1
        visited[i]=True
        i -= 1
    return list(reversed(res)),event_time_id

def main(data):
    event_time_id=0
    for content in data["datas"]:
        times,event_time_id = extract_time(content,event_time_id)
        if len(times) != 0:
            content["event"] = {
                "text_id": content["text_id"],
                "times": times
            }
    return data

