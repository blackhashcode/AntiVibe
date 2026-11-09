import sys
from collections import deque

data = sys.stdin.read().split()
N = int(data[0])
M = int(data[1])

adj = [[] for _ in range(N + 1)]
idx = 2

for _ in range(M):
    a = int(data[idx])
    b = int(data[idx+1])
    adj[a].append(b)
    idx += 2

S = int(data[idx])
T = int(data[idx+1])

INF = float('inf')
dist = [INF] * (N + 1)
dist[S] = 0

dq = deque([S])

while dq:
    u = dq.popleft()
    
    if u == T:
        print(dist[u])
        break
        
    if not adj[u]:
        continue
        
    min_neighbor = min(adj[u])
    
    for v in adj[u]:
        cost = 0 if v == min_neighbor else 1
        
        if dist[u] + cost < dist[v]:
            dist[v] = dist[u] + cost
            if cost == 0:
                dq.appendleft(v)
            else:
                dq.append(v)
else:
    print(-1)