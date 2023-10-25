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
    return ("句点" not in tags and "読点" not in tags) and ("名詞" in tags or "接尾辞" in tags or "接頭辞" in tags or "補助記号" in tags)

def combine_tango(tangos):
    """
    """
    index = 0
    while True:
        if index+1 >= len(tangos):
            break
        if is_meishi(tangos[index]) and is_meishi(tangos[index+1]):
            selif=None
            if "selif" in tangos[index]:
                selif=tangos[index]["selif"]
            elif "selif" in tangos[index+1]:
                selif=tangos[index+1]["selif"]
            tangos[index] = {
                "text": tangos[index]["text"]+tangos[index+1]["text"],
                "tag": "名詞",
#                "start_char": tangos[index]["start_char"],
#                "end_char": tangos[index+1]["end_char"],
            }
            if selif is not None:
                tangos[index]["selif"]=selif
            del tangos[index+1]
        else:
            index += 1
    return tangos

def main(data):
    for content in data["datas"]:
        for bunsetsu in content["bunsetsu"]:
            newTangos = combine_tango(bunsetsu["tokens"])
            bunsetsu["tokens"] = newTangos
        #if "selifs" in content:
        #    del content["selifs"]
        #if "blackets" in content:
        #    del content["blackets"] #とりあえずの応急処置
    return data