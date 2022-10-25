from rules.rule_loader import Rule
import re

class Bunsetsu:
    """
    文節
    """
    def __init__(self,id:int,text:str,mrph:str,parent_id:int,type1:str,type2:str) -> None:
        self.id=id
        self.text=text # 文節の内容
        self.mrph=mrph # 原型（助詞助動詞なし）
        self.parent_id=parent_id
        self.type1=type1
        self.type2=type2
    def get_joshi(self)->str:
        """
        助詞を返す
        """
        return self.text.replace(self.mrph, '').replace("、","").replace("，","").replace("。","").replace("．","")
    def match_rule(self,rule:Rule)->bool:
        if rule.types=="c": return self.mrph==rule.content #テキストを直接指定
        if rule.types=="type":return self.type1==rule.content #品詞
        if rule.types=="regex": return re.fullmatch(rule.content,self.mrph) is not None #正規表現
        return True