
from typing import List, Tuple, Dict, Set
from typing import Optional

class Rule:
    def __init__(self,name:str,types:str,content:str) -> None:
        self.name=name
        self.types=types
        self.content=content

def convert_rules(rules)->List[Rule]:
    """
    jsonファイルからRuleクラスに変換
    """
    res:List[Rule]=[]
    for rule in rules:
        if "hide" in rule and rule["hide"]: continue #使わないルールは無視
        if "_ps" in rule["name"]:#ruleの中の特殊文字列を置換
            for i in ["被告","原告"]:
                res.append(Rule(
                    rule["name"].replace("_ps",i),
                    rule["rule"]["type"],
                    rule["rule"]["c"].replace("_ps",i)
                ))
        else:
            res.append(Rule(
                rule["name"],
                rule["rule"]["type"],
                rule["rule"]["c"]
            ))
    return res

import json

def load_rules(filename:str)->List[Rule]:
    rule_file = open(filename, "r", encoding="utf-8")
    rules=json.load(rule_file)["rules"]
    rules_=convert_rules(rules)
    return rules_