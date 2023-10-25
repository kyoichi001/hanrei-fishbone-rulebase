"""

イベントとして抽出できる時間・人物の文節に係る文節にフラグを付与する

"""

import glob
from operator import is_
import os
import json
from re import T
from typing import List, Tuple, Dict, Set, Optional,Any
from value.bunsetsu import Bunsetsu, Tango
from value.graph import Graph
from value.graph import Graph


def check_rentaishi_(root: int, g: Graph, timeflagList: List[bool], personflagList: List[bool],  bnsts: List[Any]):
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


def check_rentaishi(bnsts) -> Tuple[List[bool],List[bool]]:
    timeflagList = [False for i in range(len(bnsts))]
    personflagList = [False for i in range(len(bnsts))]
    timeflagList[bnsts[-1]["id"]] = False
    personflagList[bnsts[-1]["id"]] = False
    li:List[List[int]] = [[] for i in range(len(bnsts)+1)]
    for bnst in bnsts:
        if bnst["to"] != -1:
            li[bnst["to"]].append(bnst["id"])
    g = Graph(li)
    check_rentaishi_(bnsts[-1]["id"], g, timeflagList, personflagList, bnsts)
    return timeflagList, personflagList

def main(data):
    for content in data["datas"]:
        bnsts = content["bunsetsu"]
        tt, pp = check_rentaishi(bnsts)
        for bunsetsu in content["bunsetsu"]:
            if tt[bunsetsu["id"]]:
                bunsetsu["time_kakari"] = tt[bunsetsu["id"]]
            if pp[bunsetsu["id"]]:
                bunsetsu["person_kakari"] = pp[bunsetsu["id"]]
    return data