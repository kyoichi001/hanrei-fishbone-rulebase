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
    tags=tango["tag"].split("-")
    #return "副詞可能" not in tags and ("名詞" in tags or "接尾辞" in tags or "接頭辞" in tags or "補助記号" in tags)
    return ("名詞" in tags or "接尾辞" in tags or "接頭辞" in tags or "補助記号" in tags)


def combine_tango(tangos):
    """
    """
    index = 0
    while True:
        if index+1 >= len(tangos):
            break
        if is_meishi(tangos[index]) and is_meishi(tangos[index+1]):
            tangos[index] = {
                "text": tangos[index]["text"]+tangos[index+1]["text"],
                "tag": "名詞",
#                "start_char": tangos[index]["start_char"],
#                "end_char": tangos[index+1]["end_char"],
            }
            del tangos[index+1]
        else:
            index += 1
    return tangos


def export_to_json(filepath, data):
    with open(filepath, 'w', encoding='utf8', newline='') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main(inputDir: str, outputDir: str):
    os.makedirs(outputDir, exist_ok=True)
    json_files = glob.glob(f"{inputDir}/*.json")
    for file in json_files:
        print(file)
        dat = open(file, "r", encoding="utf-8")
        data = json.load(dat)
        for content in data["contents"]["fact_reason"]["sections"]:
            if "texts" not in content:continue
            for c in content["texts"]:
                for bunsetsu in c["bunsetu"]:
                    newTangos = combine_tango(bunsetsu["tokens"])
                    bunsetsu["tokens"] = newTangos
            if "selifs" in content:
                del content["selifs"]
            if "blackets" in content:
                del content["blackets"] #とりあえずの応急処置
        output_path = os.path.splitext(os.path.basename(file))[0]
        export_to_json(f"{outputDir}/{output_path}.json", data)


if __name__ == "__main__":
    main("./02", "./03")
