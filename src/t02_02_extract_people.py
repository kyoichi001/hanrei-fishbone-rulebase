"""
時間表現に当てはまる文節のidから、その時間表現の主語を同定
"""

import glob
from operator import is_
import os
import json
from re import T
from typing import List, Tuple, Dict, Set, Optional

def extract_main_people(dat):
    """
    文から主語を抜き取る
    bnstについて、名詞と助詞のみで構成され、その助詞が「が」「は」「も」であり、is_rentaishiがfalse
    """
    res = []
    for bnst in dat["bunsetsu"]:
        if bnst.get("is_rentaishi", False) or bnst.get("person") is None:
            continue
        # if bnst.get("is_rentaishi", False):
        #    continue
        for tango in bnst["tokens"]:
            tgs=tango["tag"].split("-")
            if "名詞" not in tgs and "助詞" not in tgs:
                continue
            if tango["text"] in ["は", "が", "も"] and "助詞" in tgs:
                res.append({
                    "id": bnst["id"],
                    "person": bnst["person"]["content"],
                    "joshi": tango["text"]
                })
                break  # 単語の精査を終了し、次の文節へ
    return res

def main(data):
    for content in data["datas"]:
        # if len(content["texts"])>0:
        #    print(content["texts"][0])
        people = extract_main_people(content)
        if len(people) != 0:
            if content.get("event") is not None:
                content["event"]["people"] = people
            else:
                content["event"] = {
                    "people": people
                }
    return data