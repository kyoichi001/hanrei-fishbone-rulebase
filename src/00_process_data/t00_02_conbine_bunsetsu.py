"""
名詞・接頭詞しかない文節同士（＋隣同士の文節で、かつ直接係っている）を連結させ、一つの文節に加工する
"""

import glob
from operator import is_
import os
import json
from re import T
import csv
from typing import List, Tuple, Dict, Set, Any


def is_meishi(bst):
    """
    文節の中にある単語が名詞・接頭詞のみか
    """
    for tango in bst["tokens"]:
        tags=tango["tag"].split("-")
        if not ("名詞" in tags or "補助記号" in tags):
            return False
    return True


def merge_tree(bsts: List[Any], bst1: int, bst2: int):
    """
    bsts[bst2]をbsts[bst1]に結合する
    """
    # print(bsts[bst1])
    bsts[bst1] = {
        "id": bsts[bst1]["id"],
        "to": bsts[bst2]["to"],
        "text":bsts[bst1]["text"]+bsts[bst2]["text"],
        "tokens": bsts[bst1]["tokens"]+bsts[bst2]["tokens"]
    }
    del bsts[bst2]
    # print(bsts[bst1])
    for bst in bsts:
        if bst["id"] > bsts[bst1]["id"]:
            bst["id"] -= 1
        if bst["to"] > bsts[bst1]["id"]:
            bst["to"] -= 1
    for bst in bsts:
        if bst["to"] == bst["id"]:
            print(f"error🛑 bst.to == bst.id : {bsts}")
            break
    return bsts


def conbine_bunsetsu(bsts):
    #print("start conbining...")
    conbine_to_next = [False for i in range(len(bsts))]
    for i in range(len(bsts)-1):
        # 文節iが体言のみであれば、文節i+1に結合してもよい
        if is_meishi(bsts[i]) and bsts[i]["to"] == bsts[i+1]["id"]:
            conbine_to_next[i] = True
    index = len(bsts)-1
    while True:
        if index < 0:
            break
        #print("len bef",len(bsts))
        if conbine_to_next[index-1]:
            bsts = merge_tree(bsts, index-1, index)
            del conbine_to_next[index-1]
        index -= 1
        #print("len aft",len(bsts))
    return bsts


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
            newBsts = conbine_bunsetsu(content["bunsetsu"])
            content["bunsetsu"] = newBsts
        output_path = os.path.splitext(os.path.basename(file))[0]
        export_to_json(f"{outputDir}/{output_path}.json", data)


if __name__ == "__main__":
    main("./data", "./02")
