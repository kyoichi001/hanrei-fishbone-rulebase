
from typing import List, Tuple, Dict, Set, Any
import re

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
    def __init__(self,id:int,parent_id:int,tangos:List[Tango]) -> None:
        self.id=id
        self.parent_id=parent_id
        self.tangos=tangos
        self.is_rentaishi=False
