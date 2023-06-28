
import imp
from typing import List, Tuple, Dict, Set
from typing import Optional
from typing import Callable, Iterator, MutableMapping
from value.graph import Graph
def dfs_(from_:int,visited:List[int],g:Graph)->None:
    """
    内部用関数
    """
    for i in g.g[from_]:
        if visited[i]!=-1:continue
        visited[i]=visited[from_]+1
        dfs_(i,visited,g)

def DFS(from_:int,g:Graph)->List[int]:
    """
    頂点リストから深さ優先探索を行い、頂点間距離を返す
    """
    visited=[-1 for i in range(len(g.g))]
    visited[from_]=0
    dfs_(from_,visited,g)
    return visited
