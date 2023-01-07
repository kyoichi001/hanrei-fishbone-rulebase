"""
一つの文節の中の単語を結合させる
"""

import glob
from operator import is_
import os
import json
from re import T
import csv
from typing import List, Tuple, Dict, Set, Any


def is_meishi(tango):
    """
    文節の中にある単語が名詞・接頭詞のみか
    """
    return tango["type1"] == "名詞" or tango["type1"] == "接頭詞"


def combine_tango(tangos):
    """
    """
    index = 0
    while True:
        if index+1 >= len(tangos):
            break
        if is_meishi(tangos[index]) and is_meishi(tangos[index+1]):
            tangos[index] = {
                "content": tangos[index]["content"]+tangos[index+1]["content"],
                "type1": "名詞",
                "type2": "",
                "type3": "",
            }
            del tangos[index+1]
        else:
            tangos[index] = {
                "content": tangos[index]["content"],
                "type1":  tangos[index]["type1"],
                "type2": tangos[index]["type2"],
                "type3":  tangos[index]["type3"],
            }
            index += 1
    tangos[-1] = {
        "content": tangos[index]["content"],
        "type1":  tangos[index]["type1"],
        "type2": tangos[index]["type2"],
        "type3":  tangos[index]["type3"],
    }
    return tangos


def export_to_json(filepath, data):
    with open(filepath, 'w', encoding='utf8', newline='') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main(inputDir: str, outputDir: str):
    os.makedirs(outputDir, exist_ok=True)
    json_files = glob.glob(f"{inputDir}/*.json")
    for file in json_files:
        print(file)
        data = open(file, "r", encoding="utf-8")
        data = json.load(data)
        for content in data["contents"]:
            for dat in content["datas"]:
                for bunsetsu in dat["bunsetsu"]:
                    newTangos = combine_tango(bunsetsu["tangos"])
                    bunsetsu["tangos"] = newTangos
        output_path = os.path.splitext(os.path.basename(file))[0]
        export_to_json(f"{outputDir}/{output_path}.json", data)


if __name__ == "__main__":
    main("./02", "./03")
