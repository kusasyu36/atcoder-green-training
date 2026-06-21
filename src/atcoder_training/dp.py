"""動的計画法（DP）— ナップサック / 最長増加部分列(LIS) / 区間DP / 部分和。

■ DPとは（たとえ話）
  大きな問題を「小さな問題の答えの組み合わせ」で解く。
  一度解いた小問題の答えを表(dp)にメモして使い回すので、
  全探索だと爆発する場合でも現実的な時間で解ける。
  「同じ計算を二度しない」ための表埋め、と思えばよい。

■ DPの3要素
  1. 状態(dp[i] が何を表すか) 2. 遷移(dp[i] を前の値からどう作るか) 3. 初期値

実行:
    python -m atcoder_training.dp
"""

from __future__ import annotations

from .common import run_cases


# ─────────────────────────────────────────────────────────
# 問題1: 0-1 ナップサック
# ─────────────────────────────────────────────────────────
def knapsack(weights: list[int], values: list[int], capacity: int) -> int:
    """問題: 重さ weights・価値 values の品を、重さ合計 capacity 以内で選び価値最大に。
    各品は1個まで(0-1)。

    制約: 1 ≤ N ≤ 100, capacity ≤ 10^5
    入力例: w=[2,1,3], v=[3,2,4], cap=3 → 5（品0+品1 = 重さ3, 価値5）
    入力例: w=[1,1], v=[10,10], cap=1 → 10

    考え方: dp[w] = 重さ w 以内で得られる最大価値。品を1つずつ見て、
            重い方から更新(各品1回だけ使うため逆順ループ)。
    計算量: O(N · capacity)
    """
    dp = [0] * (capacity + 1)
    for wi, vi in zip(weights, values):
        for w in range(capacity, wi - 1, -1):   # 逆順＝同じ品を二度使わない
            dp[w] = max(dp[w], dp[w - wi] + vi)
    return dp[capacity]


# ─────────────────────────────────────────────────────────
# 問題2: 最長増加部分列（LIS）O(N log N)
# ─────────────────────────────────────────────────────────
def lis_length(a: list[int]) -> int:
    """問題: 数列 a の「狭義に増加する部分列」の最大の長さ。

    制約: 1 ≤ N ≤ 10^5
    入力例: a=[1,3,2,4] → 3（1,3,4 または 1,2,4）
    入力例: a=[5,4,3]   → 1

    考え方: tails[k] = 長さ k+1 の増加列の「末尾の最小値」。
            各要素を二分探索で置き換え、tails の長さが答え。
    計算量: O(N log N)
    """
    from bisect import bisect_left
    tails: list[int] = []
    for x in a:
        i = bisect_left(tails, x)           # x 以上の最初の位置
        if i == len(tails):
            tails.append(x)                 # 伸ばせる
        else:
            tails[i] = x                    # より小さい末尾に置き換え
    return len(tails)


# ─────────────────────────────────────────────────────────
# 問題3: 部分和（その和が作れるか）
# ─────────────────────────────────────────────────────────
def subset_sum_possible(a: list[int], target: int) -> str:
    """問題: a からいくつか選んで和を target にできるか。"Yes"/"No"。

    制約: 1 ≤ N ≤ 100, target ≤ 10^4（bit全探索が無理な規模 → DP）
    入力例: a=[3,1,4,2], target=6 → "Yes"（4+2 or 3+1+2）
    入力例: a=[3,1,4],   target=6 → "No"（作れる和は 0,1,3,4,5,7,8 のみ）

    考え方: dp[s] = 和 s が作れるか(bool)。品を見るたび、大きい方から更新。
    計算量: O(N · target)
    """
    dp = [False] * (target + 1)
    dp[0] = True                            # 何も選ばなければ和0は作れる
    for x in a:
        for s in range(target, x - 1, -1):
            if dp[s - x]:
                dp[s] = True
    return "Yes" if dp[target] else "No"


# ─────────────────────────────────────────────────────────
# 問題4: 区間DP（石取りの最小コスト＝チェーン結合の最小和の簡易版）
# ─────────────────────────────────────────────────────────
def min_merge_cost(stones: list[int]) -> int:
    """問題: 隣り合う石の山を1つにまとめると「2つの合計」のコストがかかる。
    全部を1つにするまでの合計コストの最小値。

    制約: 1 ≤ N ≤ 300（区間DP O(N^3) が間に合う規模）
    入力例: stones=[1,2,3] → 9（(1+2)=3、その後(3+3)=6、計9。順序で変わるが最小）
    入力例: stones=[5]     → 0（まとめる必要なし）

    考え方(区間DP): dp[i][j] = 区間[i,j]を1つにする最小コスト。
      dp[i][j] = min over k ( dp[i][k] + dp[k+1][j] ) + sum(i..j)。
    計算量: O(N^3)
    """
    n = len(stones)
    if n <= 1:
        return 0
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + stones[i]

    INF = float("inf")
    dp = [[0] * n for _ in range(n)]        # 長さ1の区間はコスト0
    for length in range(2, n + 1):          # 区間の長さを小さい方から
        for i in range(0, n - length + 1):
            j = i + length - 1
            best = INF
            seg = prefix[j + 1] - prefix[i]  # この区間の石の合計
            for k in range(i, j):
                best = min(best, dp[i][k] + dp[k + 1][j])
            dp[i][j] = best + seg
    return dp[0][n - 1]


def main() -> None:
    run_cases("問題1 0-1ナップサック", [
        ("w=[2,1,3],v=[3,2,4],cap=3", lambda: knapsack([2, 1, 3], [3, 2, 4], 3), 5),
        ("w=[1,1],v=[10,10],cap=1", lambda: knapsack([1, 1], [10, 10], 1), 10),
    ])
    run_cases("問題2 最長増加部分列(LIS)", [
        ("a=[1,3,2,4]", lambda: lis_length([1, 3, 2, 4]), 3),
        ("a=[5,4,3]", lambda: lis_length([5, 4, 3]), 1),
    ])
    run_cases("問題3 部分和", [
        ("a=[3,1,4,2],t=6", lambda: subset_sum_possible([3, 1, 4, 2], 6), "Yes"),
        ("a=[3,1,4],t=6", lambda: subset_sum_possible([3, 1, 4], 6), "No"),
    ])
    run_cases("問題4 区間DP(まとめる最小コスト)", [
        ("stones=[1,2,3]", lambda: min_merge_cost([1, 2, 3]), 9),
        ("stones=[5]", lambda: min_merge_cost([5]), 0),
    ])


if __name__ == "__main__":
    main()
