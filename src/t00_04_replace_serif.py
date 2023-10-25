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

def main(data):
    for content in data["datas"]:
        for bunsetsu in content["bunsetsu"]:
            for token in bunsetsu["tokens"]:
                if "selif" not in token:continue
                token["text"]=token["text"].replace("セリフ",token["selif"])
                del token["selif"]
    return data
