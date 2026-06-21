"""全探索 / bit全探索。

■ 全探索とは（たとえ話）
  「考えられる候補を、ぜんぶ試して一番良いのを選ぶ」一番素直な方法。
  頭が良くなくても、数が少なければ確実に正解できる。まず全探索を疑うのが緑への近道。

■ 計算量の感覚（ここ超大事）
  - N ≤ 10 くらい  → 2^N の bit全探索(部分集合ぜんぶ)が間に合う(2^20 ≒ 100万)
  - N ≤ 100-1000   → 二重ループ O(N^2) でも間に合うことが多い
  - N ≤ 10^5 以上  → 全探索では無理。別の工夫(累積和/二分探索/DP)が必要

実行:
    python -m atcoder_training.full_search
"""

from __future__ import annotations

from itertools import product

from .common import run_cases


# ─────────────────────────────────────────────────────────
# 問題1: ぴったりの組（二重ループの全探索）
# ─────────────────────────────────────────────────────────
def pair_sum_exists(a: list[int], target: int) -> str:
    """問題: N個の整数 a から、異なる2つを選んで和を target にできるか。

    制約: 2 ≤ N ≤ 2000（だから O(N^2) の二重ループで間に合う）
    入力例: a=[1,5,3,8], target=8 → "Yes"（3+5=8 or … ）
    入力例: a=[1,2,3],   target=7 → "No"

    考え方: i<j の全ペアを試すだけ。N≤2000 なら約200万通りで余裕。
    計算量: O(N^2)
    """
    n = len(a)
    for i in range(n):
        for j in range(i + 1, n):
            if a[i] + a[j] == target:
                return "Yes"
    return "No"


# ─────────────────────────────────────────────────────────
# 問題2: 部分集合の和（bit全探索）
# ─────────────────────────────────────────────────────────
def subset_sum_count(a: list[int], target: int) -> int:
    """問題: N個の整数から いくつか選んで(0個含む) 和を target にする選び方は何通り？

    制約: 1 ≤ N ≤ 20（2^N ≒ 100万まで → bit全探索が刺さる）
    入力例: a=[1,2,3], target=3 → 2 通り（{3} と {1,2}）
    入力例: a=[1,1,1], target=2 → 3 通り（3つから2つ選ぶ = 3通り）

    考え方: 各要素を「選ぶ/選ばない」の2択 → 全体で 2^N 通り。
            それを 0〜2^N-1 の各ビットが「選ぶ印」と見て全部試す。
    計算量: O(N · 2^N)
    """
    n = len(a)
    count = 0
    for bits in range(1 << n):              # 0 〜 2^N - 1
        s = 0
        for i in range(n):
            if bits & (1 << i):             # i番目のビットが立つ＝i番目を選ぶ
                s += a[i]
        if s == target:
            count += 1
    return count


# ─────────────────────────────────────────────────────────
# 問題3: 3つの数で最大（itertools.product で多重ループを簡潔に）
# ─────────────────────────────────────────────────────────
def max_dice_product(faces: list[int], dice: int) -> int:
    """問題: 1個の面 faces を持つサイコロを dice 回振る。出た目の積の最大は？

    制約: 1 ≤ len(faces) ≤ 6, 1 ≤ dice ≤ 5（候補は最大 6^5 ≒ 7776）
    入力例: faces=[1,2,3], dice=2 → 9（3×3）
    入力例: faces=[2],     dice=3 → 8（2×2×2）

    考え方: 全組み合わせを product で生成して積の最大を取る（多重ループの定番）。
    計算量: O(len^dice)
    """
    best = 0
    for combo in product(faces, repeat=dice):
        p = 1
        for x in combo:
            p *= x
        best = max(best, p)
    return best


def main() -> None:
    run_cases("問題1 ぴったりの組(二重ループ全探索)", [
        ("a=[1,5,3,8],t=8", lambda: pair_sum_exists([1, 5, 3, 8], 8), "Yes"),
        ("a=[1,2,3],t=7", lambda: pair_sum_exists([1, 2, 3], 7), "No"),
    ])
    run_cases("問題2 部分集合の和(bit全探索)", [
        ("a=[1,2,3],t=3", lambda: subset_sum_count([1, 2, 3], 3), 2),
        ("a=[1,1,1],t=2", lambda: subset_sum_count([1, 1, 1], 2), 3),
        ("a=[5],t=0", lambda: subset_sum_count([5], 0), 1),  # 何も選ばない1通り
    ])
    run_cases("問題3 サイコロの積の最大(product全探索)", [
        ("faces=[1,2,3],dice=2", lambda: max_dice_product([1, 2, 3], 2), 9),
        ("faces=[2],dice=3", lambda: max_dice_product([2], 3), 8),
    ])


if __name__ == "__main__":
    main()
