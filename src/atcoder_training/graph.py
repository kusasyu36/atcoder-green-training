"""グラフ — BFS / DFS / 連結成分 / 最短路(BFS)。

■ グラフとは（たとえ話）
  点(頂点)を線(辺)でつないだ地図。駅と路線、人と友達関係、部屋と扉…
  「つながり」を扱う問題は全部グラフになる。

■ BFS と DFS
  - BFS(幅優先): 近い所から波紋のように広げる。重みなしの「最短手数」に最適。
  - DFS(深さ優先): 行けるだけ奥へ進んで戻る。連結判定・全探索向き。

実行:
    python -m atcoder_training.graph
"""

from __future__ import annotations

from collections import deque

from .common import run_cases


# ─────────────────────────────────────────────────────────
# 問題1: 連結成分の数（DFS / BFS どちらでも）
# ─────────────────────────────────────────────────────────
def count_components(n: int, edges: list[tuple[int, int]]) -> int:
    """問題: 頂点 0..n-1 と無向辺 edges。グラフはいくつの「島(連結成分)」に分かれる？

    制約: 1 ≤ n ≤ 10^5
    入力例: n=5, edges=[(0,1),(1,2),(3,4)] → 2（{0,1,2} と {3,4}）
    入力例: n=3, edges=[] → 3（全部バラバラ）

    考え方: まだ訪れてない頂点から探索を始めるたびに島が1つ。探索でその島を塗る。
    計算量: O(n + 辺数)
    """
    g: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)

    seen = [False] * n
    components = 0
    for start in range(n):
        if seen[start]:
            continue
        components += 1
        stack = [start]                     # DFS をスタックで
        seen[start] = True
        while stack:
            x = stack.pop()
            for y in g[x]:
                if not seen[y]:
                    seen[y] = True
                    stack.append(y)
    return components


# ─────────────────────────────────────────────────────────
# 問題2: 重みなし最短路（BFS）
# ─────────────────────────────────────────────────────────
def shortest_steps(n: int, edges: list[tuple[int, int]], start: int, goal: int) -> int:
    """問題: 無向グラフで start から goal までの最短の辺数。到達不能なら -1。

    制約: 1 ≤ n ≤ 10^5
    入力例: n=4, edges=[(0,1),(1,2),(2,3),(0,3)], start=0, goal=2 → 2
    入力例: n=3, edges=[(0,1)], start=0, goal=2 → -1

    考え方(BFS): start から波紋状に広げ、各頂点に「何歩で着くか」を記録。
                 重みなしなら最初に着いた歩数が最短。
    計算量: O(n + 辺数)
    """
    g: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)

    dist = [-1] * n
    dist[start] = 0
    q = deque([start])
    while q:
        x = q.popleft()
        if x == goal:
            return dist[x]
        for y in g[x]:
            if dist[y] == -1:               # まだ来てない頂点だけ
                dist[y] = dist[x] + 1
                q.append(y)
    return dist[goal]


# ─────────────────────────────────────────────────────────
# 問題3: グリッド最短路（迷路BFS）
# ─────────────────────────────────────────────────────────
def maze_shortest(grid: list[str]) -> int:
    """問題: '.'は通路, '#'は壁。'S'から'G'までの最短手数。行けないなら -1。

    入力例: ["S.", ".G"] → 2
    入力例: ["S#", "#G"] → -1

    考え方: マス=頂点、隣接=辺 とみなした BFS。グリッド最短はBFSの最頻出。
    計算量: O(H·W)
    """
    h, w = len(grid), len(grid[0])
    sr = sc = gr = gc = -1
    for r in range(h):
        for c in range(w):
            if grid[r][c] == "S":
                sr, sc = r, c
            elif grid[r][c] == "G":
                gr, gc = r, c

    dist = [[-1] * w for _ in range(h)]
    dist[sr][sc] = 0
    q = deque([(sr, sc)])
    while q:
        r, c = q.popleft()
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < h and 0 <= nc < w and grid[nr][nc] != "#" and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                q.append((nr, nc))
    return dist[gr][gc]


def main() -> None:
    run_cases("問題1 連結成分の数", [
        ("n=5,[(0,1),(1,2),(3,4)]", lambda: count_components(5, [(0, 1), (1, 2), (3, 4)]), 2),
        ("n=3,[]", lambda: count_components(3, []), 3),
    ])
    run_cases("問題2 最短手数(BFS)", [
        ("0→2", lambda: shortest_steps(4, [(0, 1), (1, 2), (2, 3), (0, 3)], 0, 2), 2),
        ("到達不能", lambda: shortest_steps(3, [(0, 1)], 0, 2), -1),
    ])
    run_cases("問題3 迷路最短(グリッドBFS)", [
        ("2x2 通れる", lambda: maze_shortest(["S.", ".G"]), 2),
        ("2x2 壁で不能", lambda: maze_shortest(["S#", "#G"]), -1),
    ])


if __name__ == "__main__":
    main()
