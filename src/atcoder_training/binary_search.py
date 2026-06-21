"""二分探索 / めぐる式二分探索 / 答えで二分探索。

■ 二分探索とは（たとえ話）
  辞書で単語を探すとき、真ん中を開いて「前半か後半か」を判断し、
  半分に絞るのを繰り返す。N個から log2(N) 回で見つかる超高速探索。
  例: 100万個でも たった20回くらいで終わる（2^20 ≒ 100万）。

■ 前提
  二分探索が使えるのは「並んでいる(単調な)」もの。ソート済み配列や、
  「ある値を境にYes→Noに切り替わる」性質に対して効く。

■ めぐる式二分探索
  「条件を満たす境界」を ng(満たさない) と ok(満たす) の2点で挟み、
  真ん中 mid を試して ok/ng を更新していく書き方。境界問題に強い定番テンプレ。

実行:
    python -m atcoder_training.binary_search
"""

from __future__ import annotations

from bisect import bisect_left, bisect_right

from .common import run_cases


# ─────────────────────────────────────────────────────────
# 問題1: ソート済み配列で「x以上の最小の値」（標準ライブラリ bisect）
# ─────────────────────────────────────────────────────────
def lower_bound_value(a: list[int], x: int) -> int:
    """問題: 昇順ソート済みの a から「x 以上で最小の値」を返す。無ければ -1。

    制約: 1 ≤ N ≤ 10^5
    入力例: a=[1,3,3,7,9], x=4 → 7
    入力例: a=[1,3,3,7,9], x=3 → 3
    入力例: a=[1,2,3],     x=10 → -1

    考え方: bisect_left は「x を入れるべき左端の位置」を返す。そこが答えの位置。
    計算量: O(log N)
    """
    i = bisect_left(a, x)
    return a[i] if i < len(a) else -1


# ─────────────────────────────────────────────────────────
# 問題2: 値の個数（bisect_right - bisect_left）
# ─────────────────────────────────────────────────────────
def count_equal(a: list[int], x: int) -> int:
    """問題: 昇順ソート済みの a に x はいくつあるか。

    入力例: a=[1,3,3,3,7], x=3 → 3
    入力例: a=[1,2,4],     x=5 → 0

    考え方: 「x の右端位置 - x の左端位置」= x の個数。
    計算量: O(log N)
    """
    return bisect_right(a, x) - bisect_left(a, x)


# ─────────────────────────────────────────────────────────
# 問題3: 答えで二分探索（最大化）— めぐる式テンプレ
# ─────────────────────────────────────────────────────────
def max_pieces_length(lengths: list[int], k: int) -> int:
    """問題: 何本かの丸太 lengths を切り分けて、長さ x の棒を「k本以上」作りたい。
    作れる最大の x（整数）はいくつ？ 1本も作れないなら 0。

    制約: 1 ≤ N ≤ 10^5, 長さ ≤ 10^9
    入力例: lengths=[10,5,3], k=4 → 3（3なら 3+1+1=5本 ≥4 で足り、4だと 2+1+0=3本で足りない）
    入力例: lengths=[7],      k=3 → 2（2なら3本、3だと2本）

    考え方(答えで二分): 「長さ x で k本以上作れるか？」は x が小さいほどYesになる単調性。
      → 境界を二分探索。ok(作れる) と ng(作れない) で挟むめぐる式。
    判定 can(x): sum(L // x) ≥ k か。
    計算量: O(N log(max_len))
    """
    def can(x: int) -> bool:
        return sum(L // x for L in lengths) >= k

    ok, ng = 0, max(lengths) + 1            # ok=作れる側(x小), ng=作れない側(x大)
    while ng - ok > 1:
        mid = (ok + ng) // 2
        if can(mid):
            ok = mid
        else:
            ng = mid
    return ok


def main() -> None:
    run_cases("問題1 x以上で最小(lower_bound)", [
        ("a=[1,3,3,7,9],x=4", lambda: lower_bound_value([1, 3, 3, 7, 9], 4), 7),
        ("a=[1,3,3,7,9],x=3", lambda: lower_bound_value([1, 3, 3, 7, 9], 3), 3),
        ("a=[1,2,3],x=10", lambda: lower_bound_value([1, 2, 3], 10), -1),
    ])
    run_cases("問題2 値の個数(bisect差分)", [
        ("a=[1,3,3,3,7],x=3", lambda: count_equal([1, 3, 3, 3, 7], 3), 3),
        ("a=[1,2,4],x=5", lambda: count_equal([1, 2, 4], 5), 0),
    ])
    run_cases("問題3 答えで二分(最大の棒の長さ)", [
        ("L=[10,5,3],k=4", lambda: max_pieces_length([10, 5, 3], 4), 3),
        ("L=[7],k=3", lambda: max_pieces_length([7], 3), 2),
    ])


if __name__ == "__main__":
    main()
