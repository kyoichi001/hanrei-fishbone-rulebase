"""
文節が時間表現を含むかどうかを判定
"""

import glob
from operator import is_
import os
import json
import re
import csv
from value.time import Time
from typing import Optional
from typing import List, Tuple, Dict, Set, Any

def extract_point_time(rule, tango: str, befTime: Optional[Time]) -> Optional[Tuple[Time, str]]:
    regex = rule["regex"]
    same = rule.get("same")
    res = Time()
    a = re.search(regex, tango)
    if a is None:
        return None
    gengo_str = a.groupdict().get("gengo")
    year_str = a.groupdict().get("year")
    month_str = a.groupdict().get("month")
    day_str = a.groupdict().get("day")
    if gengo_str is not None:
        if gengo_str == "昭和":
            res.year += 1925
        elif gengo_str == "平成":
            res.year += 1988
        elif gengo_str == "令和":
            res.year += 2018
    if year_str is not None:
        if year_str == "元":
            res.year += 1
        else:
            res.year += int(year_str)
    if month_str is not None:
        res.month = int(month_str)
    if day_str is not None:
        res.day = int(day_str)
    if same is not None and befTime is not None:
        res.year = befTime.year
        res.month = befTime.month
        res.day = befTime.day
        if same == "year":
            res.year = befTime.year
        elif same == "month":
            res.month = befTime.month
        elif same == "day":
            res.day = befTime.day
    return res, a.group()

def extract_begin_time(rule, tango: str):
    regex = rule["regex"]
    a = re.search(regex, tango)
    if a is None:
        return None
    return a.group()

def extract_end_time(rule, tango: str):
    regex = rule["regex"]
    a = re.search(regex, tango)
    if a is None:
        return None
    return a.group()

def extract_other_time(rule, tango: str):
    regex = rule["regex"]
    a = re.search(regex, tango)
    if a is None:
        return None
    return a.group()

def export_to_json(filepath, data):
    with open(filepath, 'w', encoding='utf8', newline='') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def export_to_csv(filepath, data):
    import csv
    with open(filepath, 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        for row in data:
            writer.writerow(row)

def extract_times(rule, tangos: List[Any], befTime:Optional[Time]) -> Tuple[List, Optional[Time]]:
    res = []
    time = None
    for tango in tangos:
        for r in rule["point"]:
            obj = extract_point_time(r, tango["text"], befTime)
            if obj is not None:
                res.append(
                    {"type": "point", "text": obj[1], "value": obj[0].value()})
                time = obj[0]
                break
        for r in rule["begin"]:
            obj = extract_begin_time(r, tango["text"])
            if obj is not None:
                res.append({"type": "begin", "text": obj})
        for r in rule["end"]:
            obj = extract_end_time(r, tango["text"])
            if obj is not None:
                res.append({"type": "end", "text": obj})
        for r in rule["other"]:
            obj = extract_other_time(r, tango["text"])
            if obj is not None:
                res.append({"type": "other", "text": obj})
    return res, time

def main(inputDir: str, outputDir: str):
    os.makedirs(outputDir, exist_ok=True)
    files = glob.glob(f"{inputDir}/*.json")
    csv_res:List[Any] = [["id", "text_id", "bunsetsu", "text", "value"]]
    count = 0
    rule_data = open("./rules/time_rules.json", "r", encoding="utf-8")
    rule_data = json.load(rule_data)
    for file in files:
        count_b=0
        print(file)
        output_path = os.path.splitext(os.path.basename(file))[0]
        f = open(file, "r", encoding="utf-8")
        os.makedirs(outputDir+"/times_"+output_path, exist_ok=True)
        data = json.load(f)
        befTime:Optional[Time] = None
        for content in data["datas"]:
            flg=False
            for bunsetsu in content["bunsetsu"]:
                times, time = extract_times(
                    rule_data, bunsetsu["tokens"], befTime)
                if time is not None:
                    befTime = time
                if len(times) != 0:
                    bunsetsu["times"] = times
                    flg=True
                for t in times:
                    csv_res.append([count, content["text_id"], "".join(
                        [tango["text"] for tango in bunsetsu["tokens"]]), t["text"], t.get("value")])
                    count += 1
            if flg:
                export_to_json(f"{outputDir}/times_{output_path}/{str(count_b).zfill(4)}.json",content)
                count_b+=1
        export_to_json(f"{outputDir}/{output_path}.json", data)
    export_to_csv(f"{outputDir}/time_list.csv", csv_res)


if __name__ == "__main__":
    main("../00_process_data/03", "./01")
