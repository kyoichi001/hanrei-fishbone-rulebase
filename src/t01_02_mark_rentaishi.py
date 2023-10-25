"""
連体詞かどうかのフラグの付与
TMSは～し、という文節を名詞・サ変可能としてしまうので、とりあえずは名詞に係っている文節のみを連体詞とする

現状、時間・人物の抽出は、パターンが含まれるかどうかで判別しているので、
連体詞を連結させても時間と人物を検出してしまう
なので、時間と人物を検出させた後に、その文節を無視するかを処理する

"""

import glob
from operator import is_
import os
import json
from re import T
from typing import List, Tuple, Dict, Set, Optional
from value.bunsetsu import Bunsetsu, Tango
from value.graph import Graph

def check_rentaishi_(root: int, g: Graph, flagList: List[bool], bnsts: List[Bunsetsu]):
    def is_meishi(bunsetsu: Bunsetsu):
        for tango in bunsetsu.tangos:
            tgs=tango.tags.split("-")
            if "動詞" in tgs or "形容詞" in tgs or "副詞" in tgs:
                return False
        return True

    def is_rentai(bunsetsu: Bunsetsu):
        for tango in bunsetsu.tangos:
            tgs=tango.tags.split("-")
            if "連体詞" in tgs:
                return True
        return False

    def has_joshi(bunsetsu: Bunsetsu):
        for tango in bunsetsu.tangos:
            tgs=tango.tags.split("-")
            if "助詞" in tgs:
                return True
        return False
    if g.g is None: return
    children = g.g[root]
    for child in children:
        #if flagList[root] or is_rentai(bnsts[child]) or (is_meishi(bnsts[root]) and not has_joshi(bnsts[child])):
        if flagList[root] or is_rentai(bnsts[child]) or is_meishi(bnsts[root]):
            flagList[child] = True
        check_rentaishi_(child, g, flagList, bnsts)


def check_rentaishi(bnsts: List[Bunsetsu]) -> List[bool]:
    #print("check root")
    flagList = [False for i in range(len(bnsts))]
    flagList[bnsts[-1].id] = False
    li:list[list[int]] = [[] for i in range(len(bnsts)+1)]
    for bnst in bnsts:
        if bnst.to != -1:
            li[bnst.to].append(bnst.id)
    g = Graph(li)
    check_rentaishi_(bnsts[-1].id, g, flagList, bnsts)
    for bnst in bnsts:
        bnst.is_rentaishi = flagList[bnst.id]
    return flagList

def main(data):
    import sys
    for content in data["datas"]:
        try:
            bnsts: List[Bunsetsu] = [Bunsetsu(
                bnst["id"],
                bnst["to"],
                [Tango(tango["text"], tango["tag"]) for tango in bnst["tokens"]]
            ) for bnst in content["bunsetsu"]]
            b = check_rentaishi(bnsts)
            for bunsetsu in content["bunsetsu"]:
                if b[bunsetsu["id"]]:
                    bunsetsu["is_rentaishi"] = b[bunsetsu["id"]]
        except RecursionError as e:
            print(content["bunsetsu"],file=sys.stderr)
    return data
