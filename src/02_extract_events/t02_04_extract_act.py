"""
行動の抽出
人物から文末、時間表現もしくは人物の文節までの動詞を抽出
そこから人物に関連した時間表現の文節を排除
"""

"""

"event": {
    "text_id": 22,
    "times": [
        {
            "id": 1,
            "text": "平成２８年４月２６日",
            "value": 20160426
        }
    ],
    "people": [
        {
            "id": 0,
            "person": "被告",
            "joshi": "は"
        }
    ]
    "acts":[
        "ids":[],
        "text":"***"
    ]
}
"""




import csv
import glob
from operator import is_
import os
import json
from typing import List, Tuple, Dict, Set, Optional, Any
def export_to_json(filepath, data):
    with open(filepath, 'w', encoding='utf8', newline='') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def extract_events(dat):
    res = []
    for bnst in dat["bunsetsu"]:
        if bnst["is_rentaishi"]:
            continue
        for tango in bnst["tangos"]:
            if tango["type1"] == "動詞":
                res.append({
                    "id": bnst["id"],
                    "tangos": "".join([tango["content"] for tango in bnst["tangos"]])
                })
                break  # 単語の精査を終了し、次の文節へ
    return res


def extract_events_2(dat):
    """

    """
    def is_shugo(bst):
        if bst.get("is_rentaishi", False) or bst.get("person") is None:
            return False
        for tango in bst["tangos"]:
            if tango["content"] in ["は", "が", "も"] and tango["type1"] == "助詞":
                return True
        return False
    res = []
    extracts = False
    for bnst in dat["bunsetsu"]:
        if bnst.get("times") is None:
            continue
        for time in bnst["times"]:
            if time["type"] == "point":
                extracts = True
                break
    if not extracts:
        return []
    extract_time = None
    acts: str = ""
    person = ""
    for bnst in dat["bunsetsu"]:
        if bnst.get("time_kakari", False) or bnst.get("person_kakari", False):
            continue  # 時間か人物に係る文節なら行動として抽出しない
        if bnst.get("is_rentaishi", False):  # 連体詞であれば、人物か時間かの判定をせず、行動に追加
            acts += "".join([tango["content"] for tango in bnst["tangos"]])
            continue
            pass
        if bnst.get("times") is not None:
            t = None
            for time in bnst["times"]:
                if time["type"] == "point":
                    t = "".join([t_obj["text"] for t_obj in bnst["times"]])
                    break
            if t is not None:  # 時間表現（値があるやつ）がくれば行動の抽出を終了
                if extract_time is not None:  # すでにイベントを抽出していれば、抽出したイベントを出力に渡す
                    res.append({
                        "person": person,
                        "time": extract_time,
                        "acts": acts
                    })
                    acts = ""
                    person = ""
                extract_time = t
            continue
        if bnst.get("person") is not None:  # 人物がくれば行動の抽出を終了
            if not is_shugo(bnst):  # 主語でない場合スルー
                acts += "".join([tango["content"] for tango in bnst["tangos"]])
                continue
            if person != "":  # すでに人物を抽出していれば、抽出したイベントを出力に渡す
                res.append({
                    "person": person,
                    "time": extract_time,
                    "acts": acts
                })
                extract_time = None
                acts = ""
            person = bnst["person"]["content"]
            continue
        acts += "".join([tango["content"] for tango in bnst["tangos"]])
    if extract_time is not None and person != "":  # すでにイベントを抽出していれば、抽出したイベントを出力に渡す
        res.append({
            "person": person,
            "time": extract_time,
            "acts": acts
        })
    return res


def export_events_to_csv(output_path, csv_datas):
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for d in csv_datas:
            writer.writerow(d)


def main(inputDir: str, outputDir: str):
    os.makedirs(outputDir, exist_ok=True)
    files = glob.glob(f"{inputDir}/*.json")
    for file in files:
        csv_results = [["id",  "person", "time", "act"]]
        print(file)
        output_path = os.path.splitext(os.path.basename(file))[0]
        index = 0
        data = open(file, "r", encoding="utf-8")
        data = json.load(data)
        for content in data["contents"]:
            tts = {}
            for d in content["texts"]:
                tts[d["text_id"]] = d["text"]
            for dat in content["datas"]:
                if dat.get("event") is None:
                    continue
                if dat["event"].get("times") is None:
                    continue
                ddd = extract_events_2(dat)
                if len(ddd) != 0:
                    dat["events"] = ddd
                for e in ddd:
                    if e["person"] == "" or e["time"] == "" or e["time"] is None or e["acts"] == "":
                        continue
                    # print(e)
                    csv_results.append([
                        index,
                        e["person"],
                        e["time"],
                        e["acts"]
                    ])
                    index += 1
        export_to_json(f"{outputDir}/{output_path}.json", data)
        export_events_to_csv(f"./p03/{output_path}.csv", csv_results)


if __name__ == "__main__":
    main("./03", "./04")
