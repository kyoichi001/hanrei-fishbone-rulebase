"""
複数の文節で一つの時間表現となる文節に time_group プロパティを追加

時間表現をもつ文節に直接時間表現の文節が係る場合、time_groupという判定とする
"""

import glob
from operator import is_
import os
import json
import re
from re import T
from typing import List, Tuple, Dict, Set,Optional,Any
from value.bunsetsu import Bunsetsu,Tango,Sentence
from value.event import Event
from value.graph import Graph

"""
root がtime_groupをなすかどうか判定する
time_groupをつくる場合、同じtime_groupの文節IDのリストを得る

DFSで係り受けが隣接している時間表現をグループ化
"""
def add_time_group_(root: int, g: Graph, group_list: List[List[int]], bnsts: List[Any]):
    def has_value(bnst:Any):
        for t in bnst["times"]:
            if t["type"]=="point":return True
        return False
    children = g.g[root]
    if "times" in bnsts[root]:
        print("!!!!!!!!!!!")
        group_list[root].append(root)
    for child in children:
        add_time_group_(child, g, group_list, bnsts)
        if "times" in bnsts[root] and "times" in bnsts[child]: #係り先に時間があり、かつ自分にも時間があるならグループ化する
            if not has_value(bnsts[root]) and not has_value(bnsts[child]):continue
            print("!!!!!!!!!!!")
            group_list[root].extend(group_list[child])

def add_time_group(bsts:list[Any]):
    group_list:list[list[int]] = [[] for i in range(len(bsts))]
    li:list[list[int]] = [[] for i in range(len(bsts)+1)]
    for bnst in bsts:
        if bnst["to"] != -1:
            li[bnst["to"]].append(bnst["id"])
    g = Graph(li)
    print(bsts[0])
    add_time_group_(bsts[-1]["id"], g, group_list, bsts)
    for bnst in bsts:
        if len(group_list[bnst["id"]])>1:
            bnst["time_group"] = group_list[bnst["id"]]

def main(data):
    contents =data["datas"]
    for content in contents:
        #if len(content["texts"])>0:
        #    print(content["texts"][0])
        add_time_group(content["bunsetsu"])
    return data