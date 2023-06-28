
from typing import List, Tuple, Dict, Set, Any
import re
from .event import Event
from .graph import Graph
from typing import List, Tuple, Dict, Set,Optional

class TimeAttribute:
    def __init__(self,text:str,value:int):
        self.text=text
        self.value=value
class PersonAttribute:
    def __init__(self,content:str):
        self.content=content
class ReplaceSelif:
    """
    本文にある「セリフ」を置き換えるためのデータ
    """
    def __init__(self,target_selif:int,content:str,target_text_id:int,text_id:int) -> None:
          self.target_selif=target_selif # そのテキストの何番目の「セリフ」か
          self.content=content
          self.target_text_id=target_text_id
          self.text_id=text_id
class ReplaceBlacket:
    """
    本文にある（）を挿入するためのデータ
    """
    def __init__(self,position:int,content:str,target_text_id:int,text_id:int) -> None:
          self.position=position
          self.content=content
          self.target_text_id=target_text_id
          self.text_id=text_id
class Text:
    def __init__(self,text_id:int,text:int) -> None:
        self.text_id=text_id
        self.text=text

class Tango:
    """
    単語
    """
    def __init__(self,content,type1,type2,type3):
        self.content=content
        self.type1=type1
        self.type2=type2
        self.type3=type3

class Bunsetsu:
    """
    文節
    """
    def __init__(self,id:int,to:int,tangos:List[Tango],is_rentaishi=False,time:TimeAttribute=None,person:PersonAttribute=None) -> None:
        self.id=id
        self.to=to
        self.tangos=tangos
        self.is_rentaishi=is_rentaishi
        self.time=time
        self.person=person

class Sentence:
    """
    文についてのクラス（文節のリスト）
    """
    def __init__(self,text_id:int,bnsts:List[Bunsetsu],events:Optional[List[Event]]) -> None:
        self.text_id=text_id
        self.bnsts=bnsts
        self.events=events
    def get_graph(self)->Graph:
        """
        文節のグラフを返す
        """
        res=[[] for i in self.bnsts]
        for bnst in self.bnsts:
            if bnst.parent_id==-1:
                continue
            else:
                res[bnst.id-1].append(bnst.parent_id-1)
                res[bnst.parent_id-1].append(bnst.id-1)
        return Graph(res)

class HanreiContents:
    """
    jsonのcontentsの型定義
    """
    def __init__(self,type:str,header:str,texts:List[Text],selifs:Optional[List[ReplaceSelif]],blackets:Optional[List[ReplaceBlacket]],datas:List[Sentence]):
      self.type=type
      self.header=header
      self.texts=texts
      self.selifs=selifs
      self.blackets=blackets
      self.datas=datas

def convert_json2class(data):
    """
    jsonファイルをクラスに変換
    """

def convert_class2json(data):
    """
    クラスをjsonファイル用の辞書に変換
    """