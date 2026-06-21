"""ダイクストラ法 / Union-Find（DSU）。

■ ダイクストラ（たとえ話）
  「辺ごとに移動コスト(距離・料金)が違う」地図で、最短コストを求める。
  今いちばん近い未確定の点から確定させていく(優先度付きキューを使う)。
  ※辺のコストが負だと使えない(その場合はベルマンフォード)。

■ Union-Find / DSU（たとえ話）
  「この2人は同じグループ？」を超高速で答えるデータ構造。
  各グループの“代表者”を辿れるようにし、つなぐ(union)と判定(find)を almost O(1) で。
  連結判定・グループ分け・最小全域木(クラスカル法)の土台。

実行:
    python -m atcoder_training.dijkstra_unionfind
"""

from __future__ import annotations

import heapq

from .common import run_cases


# ─────────────────────────────────────────────────────────
# 問題1: ダイクストラ（重み付き最短路）
# ─────────────────────────────────────────────────────────
def dijkstra(n: int, edges: list[tuple[int, int, int]], start: int, goal: int) -> int:
    """問題: 重み付き無向グラフ(辺 (u,v,コスト))で start→goal の最小コスト。不能なら -1。

    制約: 1 ≤ n ≤ 10^5, コスト ≥ 0
    入力例: n=4, edges=[(0,1,1),(1,2,5),(0,2,2),(2,3,1)], 0→3 → 3（0-2-3）
    入力例: n=2, edges=[], 0→1 → -1

    考え方: dist[start]=0 から、優先度付きキューで「今いちばん近い点」を取り出して確定し、
            隣を更新。確定済みより大きい古い値はスキップ。
    計算量: O((n+辺数) log n)
    """
    g: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
        g[v].append((u, w))

    INF = float("inf")
    dist = [INF] * n
    dist[start] = 0
    pq: list[tuple[int, int]] = [(0, start)]   # (今までのコスト, 頂点)
    while pq:
        d, x = heapq.heappop(pq)
        if d > dist[x]:                        # 古い(更新済みより悪い)情報は捨てる
            continue
        for y, w in g[x]:
            nd = d + w
            if nd < dist[y]:
                dist[y] = nd
                heapq.heappush(pq, (nd, y))
    return dist[goal] if dist[goal] != INF else -1


# ─────────────────────────────────────────────────────────
# 問題2: Union-Find 本体
# ─────────────────────────────────────────────────────────
class UnionFind:
    """グループ分けを almost O(1) で扱う定番データ構造（経路圧縮＋ランク併合）。"""

    def __init__(self, n: int) -> None:
        self.parent = list(range(n))        # 最初は全員が自分自身の代表
        self.size = [1] * n

    def find(self, x: int) -> int:
        """x の属するグループの代表を返す（経路圧縮で次回以降を速くする）。"""
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]  # 親を祖父に付け替え
            x = self.parent[x]
        return x

    def union(self, x: int, y: int) -> None:
        """x と y を同じグループにする（小さい方を大きい方へ繋ぐ）。"""
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return
        if self.size[rx] < self.size[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        self.size[rx] += self.size[ry]

    def same(self, x: int, y: int) -> bool:
        """x と y は同じグループ？"""
        return self.find(x) == self.find(y)

    def group_size(self, x: int) -> int:
        """x の属するグループの人数。"""
        return self.size[self.find(x)]


# ─────────────────────────────────────────────────────────
# 問題3: Union-Find の利用（友達関係のグループ判定）
# ─────────────────────────────────────────────────────────
def friends_same_group(n: int, relations: list[tuple[int, int]],
                       queries: list[tuple[int, int]]) -> list[str]:
    """問題: n人。relations で2人を友達にする(友達の友達も同じグループ)。
    各クエリ (a,b) が同じグループかを "Yes"/"No" で答える。

    入力例: n=4, relations=[(0,1),(1,2)], queries=[(0,2),(0,3)] → ["Yes","No"]

    考え方: union で繋ぎ、same で判定するだけ。Union-Find の典型用途。
    計算量: ほぼ O((relations + queries) · α(n))（α はほぼ定数）
    """
    uf = UnionFind(n)
    for a, b in relations:
        uf.union(a, b)
    return ["Yes" if uf.same(a, b) else "No" for (a, b) in queries]


def main() -> None:
    run_cases("問題1 ダイクストラ(重み付き最短)", [
        ("0→3", lambda: dijkstra(4, [(0, 1, 1), (1, 2, 5), (0, 2, 2), (2, 3, 1)], 0, 3), 3),
        ("到達不能", lambda: dijkstra(2, [], 0, 1), -1),
    ])
    run_cases("問題2 UnionFind 基本動作", [
        ("union後same", lambda: (lambda uf: (uf.union(0, 1), uf.union(1, 2), uf.same(0, 2))[-1])(UnionFind(4)), True),
        ("別グループ", lambda: (lambda uf: (uf.union(0, 1), uf.same(0, 3))[-1])(UnionFind(4)), False),
        ("グループ人数", lambda: (lambda uf: (uf.union(0, 1), uf.union(1, 2), uf.group_size(0))[-1])(UnionFind(4)), 3),
    ])
    run_cases("問題3 友達グループ判定", [
        ("queries", lambda: friends_same_group(4, [(0, 1), (1, 2)], [(0, 2), (0, 3)]), ["Yes", "No"]),
    ])


if __name__ == "__main__":
    main()
