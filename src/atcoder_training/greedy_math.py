"""貪欲法 / 数学（GCD・LCM / エラトステネスの篩 / 繰り返し二乗法）。

■ 貪欲法とは（たとえ話）
  「その場で一番得な選択」を繰り返す。いつでも正しいわけではないが、
  正しいと証明できる問題では最速・最短コードになる。例: 締切順・コスト順に処理。

■ 数学の道具
  - GCD/LCM: 最大公約数・最小公倍数。分数や周期の問題で多用。
  - エラトステネスの篩: N以下の素数を一気に列挙する高速法。
  - 繰り返し二乗法(modpow): a^b mod m を O(log b) で。巨大な累乗の定番。

実行:
    python -m atcoder_training.greedy_math
"""

from __future__ import annotations

from math import gcd

from .common import run_cases


# ─────────────────────────────────────────────────────────
# 問題1: 区間スケジューリング（貪欲：終了時刻が早い順）
# ─────────────────────────────────────────────────────────
def max_non_overlap(intervals: list[tuple[int, int]]) -> int:
    """問題: 区間 [開始, 終了) の集合から、重ならないように最大何個選べるか。

    制約: 1 ≤ N ≤ 10^5
    入力例: [(0,2),(1,3),(2,4)] → 2（[0,2) と [2,4)）
    入力例: [(0,5),(1,2),(2,3)] → 2（[1,2) と [2,3)）

    考え方(貪欲): 「終了が早い順」に並べ、前に選んだ終了以降に始まる区間を貪欲に取る。
                 終了が早いほど後の余地が増える、というのが正しさの理由。
    計算量: O(N log N)
    """
    intervals = sorted(intervals, key=lambda x: x[1])   # 終了時刻でソート
    count = 0
    current_end = -float("inf")
    for s, e in intervals:
        if s >= current_end:                # 前の予定と重ならないなら取る
            count += 1
            current_end = e
    return count


# ─────────────────────────────────────────────────────────
# 問題2: LCM（最小公倍数）— GCD から作る
# ─────────────────────────────────────────────────────────
def lcm_of_list(a: list[int]) -> int:
    """問題: 整数リスト a 全部の最小公倍数(LCM)を返す。

    入力例: [4,6] → 12
    入力例: [2,3,4] → 12

    考え方: lcm(x,y) = x*y // gcd(x,y)。これを畳み込む。
    計算量: O(N log(max))
    """
    result = a[0]
    for x in a[1:]:
        result = result * x // gcd(result, x)
    return result


# ─────────────────────────────────────────────────────────
# 問題3: エラトステネスの篩（素数列挙）
# ─────────────────────────────────────────────────────────
def primes_upto(n: int) -> list[int]:
    """問題: n 以下の素数を昇順で全部返す。

    制約: n ≤ 10^7 程度まで現実的
    入力例: n=10 → [2,3,5,7]
    入力例: n=1  → []

    考え方: 2から順に「その倍数」を消していく。残ったのが素数。
    計算量: O(n log log n)
    """
    if n < 2:
        return []
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    p = 2
    while p * p <= n:
        if is_prime[p]:
            for multiple in range(p * p, n + 1, p):   # p*p から始めてよい
                is_prime[multiple] = False
        p += 1
    return [i for i in range(2, n + 1) if is_prime[i]]


# ─────────────────────────────────────────────────────────
# 問題4: 繰り返し二乗法（a^b mod m）
# ─────────────────────────────────────────────────────────
def mod_pow(a: int, b: int, m: int) -> int:
    """問題: a の b 乗を m で割った余りを高速に求める。

    制約: b は 10^18 でも可（普通に掛けると無理 → log b 回で）
    入力例: a=2, b=10, m=1000 → 24（1024 % 1000）
    入力例: a=3, b=0,  m=7    → 1（何でも0乗は1）

    考え方: 指数を2進数で見て「2乗を繰り返しながら、ビットが立つ所だけ掛ける」。
    計算量: O(log b)
    """
    result = 1
    a %= m
    while b > 0:
        if b & 1:                           # 今のビットが立っていれば掛ける
            result = result * a % m
        a = a * a % m                       # 底を2乗
        b >>= 1                             # 次のビットへ
    return result


def main() -> None:
    run_cases("問題1 区間スケジューリング(貪欲)", [
        ("[(0,2),(1,3),(2,4)]", lambda: max_non_overlap([(0, 2), (1, 3), (2, 4)]), 2),
        ("[(0,5),(1,2),(2,3)]", lambda: max_non_overlap([(0, 5), (1, 2), (2, 3)]), 2),
    ])
    run_cases("問題2 最小公倍数(LCM)", [
        ("[4,6]", lambda: lcm_of_list([4, 6]), 12),
        ("[2,3,4]", lambda: lcm_of_list([2, 3, 4]), 12),
    ])
    run_cases("問題3 素数列挙(エラトステネス)", [
        ("n=10", lambda: primes_upto(10), [2, 3, 5, 7]),
        ("n=1", lambda: primes_upto(1), []),
    ])
    run_cases("問題4 繰り返し二乗法(modpow)", [
        ("2^10%1000", lambda: mod_pow(2, 10, 1000), 24),
        ("3^0%7", lambda: mod_pow(3, 0, 7), 1),
    ])


if __name__ == "__main__":
    main()
