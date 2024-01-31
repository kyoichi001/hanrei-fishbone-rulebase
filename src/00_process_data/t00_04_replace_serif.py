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
        for content in data["datas"]:
            for bunsetsu in content["bunsetsu"]:
                has_selif=False
                for token in bunsetsu["tokens"]:
                    if "selif" not in token:continue
                    token["text"]=token["text"].replace("セリフ",token["selif"])
                    del token["selif"]
                    has_selif=True
                if has_selif:
                    bunsetsu["text"]="".join([token["text"] for token in bunsetsu["tokens"]])
        output_path = os.path.splitext(os.path.basename(file))[0]
        export_to_json(f"{outputDir}/{output_path}.json", data)

if __name__ == "__main__":
    main("./03", "./04")
