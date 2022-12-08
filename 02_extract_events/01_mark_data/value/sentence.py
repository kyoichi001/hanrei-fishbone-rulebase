from value.bunsetsu import Bunsetsu
from value.event import Event
from typing import List, Tuple, Dict, Set,Optional
from value.graph import Graph

class Sentence:
    """
    文についてのクラス（文節のリスト）
    """
    def __init__(self,bnsts:List[Bunsetsu],events:List[Event]) -> None:
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