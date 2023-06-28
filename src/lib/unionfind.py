from collections import defaultdict
from typing import List

class UnionFind():
    def __init__(self, n:int):
        self.n = n
        self.parents = [-1] * n

    def find(self, x:int)->int:
        if self.parents[x] < 0:
            return x
        else:
            self.parents[x] = self.find(self.parents[x])
            return self.parents[x]

    def union(self, x:int, y:int):
        x = self.find(x)
        y = self.find(y)

        if x == y:
            return

        if self.parents[x] > self.parents[y]:
            x, y = y, x

        self.parents[x] += self.parents[y]
        self.parents[y] = x

    def size(self, x:int)->int:
        return -self.parents[self.find(x)]

    def same(self, x:int, y:int)->bool:
        return self.find(x) == self.find(y)

    def members(self, x:int)->List[int]:
        root = self.find(x)
        return [i for i in range(self.n) if self.find(i) == root]

    def roots(self)->List[int]:
        return [i for i, x in enumerate(self.parents) if x < 0]

    def group_count(self)->int:
        return len(self.roots())

    def all_group_members(self)->defaultdict[int,list]:
        group_members = defaultdict(list)
        for member in range(self.n):
            group_members[self.find(member)].append(member)
        return group_members

    def __str__(self):
        return '\n'.join(f'{r}: {m}' for r, m in self.all_group_members().items())