"""

イベントとして抽出できる時間・人物の文節に係る文節にフラグを付与する

"""

import glob
from operator import is_
import os
import json
from re import T
from typing import List, Tuple, Dict, Set, Optional
from value.bunsetsu import Bunsetsu, Tango
from value.graph import Graph
from value.graph import Graph


def check_rentaishi_(root: int, g: Graph, timeflagList: List[bool], personflagList: List[bool],  bnsts: List[Bunsetsu]):
    children = g.g[root]
    # print(bnsts[root])
    if personflagList[root] or bnsts[root].get("person") is not None:
        for child in children:
            personflagList[child] = True
    if timeflagList[root] or (bnsts[root].get("times") is not None and "point" in [time["type"] for time in bnsts[root]["times"]]):
        for child in children:
            timeflagList[child] = True
    for child in children:
        check_rentaishi_(child, g, timeflagList, personflagList, bnsts)


def check_rentaishi(bnsts) -> List[bool]:
    timeflagList = [False for i in range(len(bnsts))]
    personflagList = [False for i in range(len(bnsts))]
    timeflagList[bnsts[-1]["id"]] = False
    personflagList[bnsts[-1]["id"]] = False
    li = [[] for i in range(len(bnsts)+1)]
    for bnst in bnsts:
        if bnst["to"] != -1:
            li[bnst["to"]].append(bnst["id"])
    g = Graph(li)
    check_rentaishi_(bnsts[-1]["id"], g, timeflagList, personflagList, bnsts)
    return timeflagList, personflagList


def export_to_json(filename: str, data) -> None:
    with open(filename, 'w', encoding='utf8', newline='') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main(inputDir: str, outputDir: str):
    os.makedirs(outputDir, exist_ok=True)
    files = glob.glob(f"{inputDir}/*.json")
    for file in files:
        print(file)
        data = open(file, "r", encoding="utf-8")
        data = json.load(data)
        for content in data["contents"]:
            for d in content["datas"]:
                bnsts = d["bunsetsu"]
                tt, pp = check_rentaishi(bnsts)
                for bunsetsu in d["bunsetsu"]:
                    if tt[bunsetsu["id"]]:
                        bunsetsu["time_kakari"] = tt[bunsetsu["id"]]
                    if pp[bunsetsu["id"]]:
                        bunsetsu["person_kakari"] = pp[bunsetsu["id"]]
        output_path = os.path.splitext(os.path.basename(file))[0]
        export_to_json(f"{outputDir}/{output_path}.json", data)


if __name__ == "__main__":
    main("./02", "./03")
