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


def extract_time(dat: Any):
    res = []
    time_obj:Any = {
        "bnst_ids": [],
        "span_text": {},
        "span_value": {}
    }
    mode = "point"
    i = len(dat["bunsetsu"])-1
    extracting = False
    while i >= 0:  # 文節を後ろから見る
        mode = "point"  # 文節が変わったので、時間のフラグをリセット
        bnst = dat["bunsetsu"][i]
        if not bnst.get("is_rentaishi", False) and bnst.get("times") is not None:
            # 連体詞でないかつtimesプロパティを持つなら、出力の文節idリストに追加し、抽出フラグを立てる
            time_obj["bnst_ids"].append(i)
            extracting = True
        elif extracting:
            if bnst.get("is_rentaishi", False) and bnst.get("times") is not None:
                # 文節が連体詞であっても、時間表現をもち、かつ抽出が継続している場合
                time_obj["bnst_ids"].append(i)
            else:
                # 抽出の条件が切れたらリセット
                if len(list(time_obj["span_value"].keys())) != 0:
                    res.append(time_obj)
                time_obj = {
                    "bnst_ids": [],
                    "span_text": {},
                    "span_value": {}
                }
                mode = "point"
                extracting = False
        if extracting:
            for time in reversed(bnst["times"]):
                if time["type"] == "point":
                    time_obj["span_text"][mode] = time["text"]
                    time_obj["span_value"][mode] = time["value"]
                    mode = "point"
                elif time["type"] == "begin" and mode == "point":
                    mode = "begin"
                elif time["type"] == "end" and mode == "point":
                    mode = "end"
                elif time["type"] == "other":
                    pass
        i -= 1
    if extracting:
        res.append(time_obj)
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
        data = {}
        with open(file, encoding="utf-8") as f:
            data = json.load(f)
        for content in data["contents"]:
            for dat in content["datas"]:
                times = extract_time(dat)
                if len(times) != 0:
                    dat["event"] = {
                        "text_id": dat["text_id"],
                        "times": times
                    }
        export_to_json(f"{outputDir}/{output_path}.json", data)


if __name__ == "__main__":
    main("../01_mark_data/03", "01")
