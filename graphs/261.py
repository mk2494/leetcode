'''
	problem link : https://leetcode.com/problems/graph-valid-tree/
'''

'''
approach 1 - dfs with cycle detection in undirected graph
time - O(V+E)
space - O(V+E)
'''
class Solution:
    WHITE = 1
    GRAY = 2
    BLACK = 3
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        if n == 1 and not edges:
            return True
        
        if len(edges)!=n-1:
            return False
        
        graph = collections.defaultdict(list)
        
        for edge in edges:
            src, dst = edge
            graph[src].append(dst)
            graph[dst].append(src)
        
        color = {c:self.WHITE for c in range(0,n)}
        visited = set()
        
        def dfs(node, parent):
            visited.add(node)
            color[node]=self.GRAY
            if node in graph:
                for nei in graph[node]:
                    if color[nei]==self.GRAY and nei!=parent:
                        return False
                    if color[nei]==self.WHITE:
                        result = dfs(nei, node)
                        if not result:
                            return False
            color[node]=self.BLACK
            return True
        
        dfs(0, None)
        return len(visited)==n

'''
approach 2 - unoptimized version of union - find algorithm
time : O(N^2) for each of (n-1) edges, union takes O(n) time 
as the tree could get bigger and skewed.
space: O(N)
'''
class UnionFind:
    
    def __init__(self, n):
        self.parent = [node for node in range(n)]
    
    def find(self, A):
        while A != self.parent[A]:
            A = self.parent[A]
        return A
    
    def union(self, A, B):
        root_A = self.find(A)
        root_B = self.find(B)
        # means cycle - as already connected
        if root_A == root_B:
            return False
        self.parent[root_A] = root_B
        return True

class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        if len(edges) != n - 1: return False
        unionFind = UnionFind(n)
        for A, B in edges:
            if not unionFind.union(A, B):
                return False
        # no cycles found yet, return True
        return True

'''
approach 3: path compression and union by rank
time : O(N * a(N)) where a is reverse ackermann function
N ~ order of number of edges
space : O(N)
'''
class UnionFind:
    
    def __init__(self, n):
        self.parent = {c:c for c in range(n)}
        self.size = [1]*n
    
    def find(self, A):
        root = A
        while root != self.parent[root]:
            root = self.parent[root]
        while A != root:
            old_root = self.parent[A]
            self.parent[A] = root
            A = old_root
        return root
    
    def union(self, A, B):
        rootA = self.find(A)
        rootB = self.find(B)
        # cycle
        if rootA == rootB:
            return False
        if self.size[rootA] > self.size[rootB]:
            self.parent[rootB] = rootA
            self.size[rootA] += self.size[rootB]
        else:
            self.parent[rootA] = rootB
            self.size[rootB] += self.size[rootA]
        return True
                         
class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        if len(edges) != n-1:
            return False
        uf = UnionFind(n)
        for edge in edges:
            src, dst = edge
            if not uf.union(src, dst):
                return False
        # no cycles
        return True