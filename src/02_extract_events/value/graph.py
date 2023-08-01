from typing import List, Tuple, Dict, Set,Optional
class Graph:
    """
    隣接リストをグラフとして保持するクラス
    """
    def __init__(self,g:List[List[int]]) -> None:
        """
        隣接リストで初期化
        """
        self.g=g
