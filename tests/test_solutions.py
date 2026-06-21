"""各テーマの模範解を、入出力例＋エッジケースで検証する。"""

from atcoder_training.full_search import (
    max_dice_product, pair_sum_exists, subset_sum_count,
)
from atcoder_training.binary_search import (
    count_equal, lower_bound_value, max_pieces_length,
)
from atcoder_training.cumulative_sum import imos_overlaps, range_sums, rect_sum
from atcoder_training.dp import (
    knapsack, lis_length, min_merge_cost, subset_sum_possible,
)
from atcoder_training.graph import count_components, maze_shortest, shortest_steps
from atcoder_training.dijkstra_unionfind import (
    UnionFind, dijkstra, friends_same_group,
)
from atcoder_training.greedy_math import (
    lcm_of_list, max_non_overlap, mod_pow, primes_upto,
)


# ── full_search ──
def test_pair_sum():
    assert pair_sum_exists([1, 5, 3, 8], 8) == "Yes"
    assert pair_sum_exists([1, 2, 3], 7) == "No"


def test_subset_sum_count():
    assert subset_sum_count([1, 2, 3], 3) == 2
    assert subset_sum_count([1, 1, 1], 2) == 3
    assert subset_sum_count([5], 0) == 1          # 何も選ばない


def test_max_dice_product():
    assert max_dice_product([1, 2, 3], 2) == 9
    assert max_dice_product([2], 3) == 8


# ── binary_search ──
def test_lower_bound():
    assert lower_bound_value([1, 3, 3, 7, 9], 4) == 7
    assert lower_bound_value([1, 3, 3, 7, 9], 3) == 3
    assert lower_bound_value([1, 2, 3], 10) == -1


def test_count_equal():
    assert count_equal([1, 3, 3, 3, 7], 3) == 3
    assert count_equal([1, 2, 4], 5) == 0


def test_max_pieces_length():
    assert max_pieces_length([10, 5, 3], 4) == 3
    assert max_pieces_length([7], 3) == 2
    assert max_pieces_length([1], 5) == 0          # 5本も作れない


# ── cumulative_sum ──
def test_range_sums():
    assert range_sums([1, 2, 3, 4], [(0, 2), (1, 3)]) == [6, 9]
    assert range_sums([5], [(0, 0)]) == [5]


def test_imos():
    assert imos_overlaps(5, [(0, 2), (1, 3)]) == [1, 2, 2, 1, 0]


def test_rect_sum():
    assert rect_sum([[1, 2], [3, 4]], 0, 0, 1, 1) == 10
    assert rect_sum([[1, 2, 3], [4, 5, 6]], 0, 1, 1, 2) == 16


# ── dp ──
def test_knapsack():
    assert knapsack([2, 1, 3], [3, 2, 4], 3) == 5
    assert knapsack([1, 1], [10, 10], 1) == 10


def test_lis():
    assert lis_length([1, 3, 2, 4]) == 3
    assert lis_length([5, 4, 3]) == 1
    assert lis_length([1, 1, 1]) == 1              # 狭義増加なので1


def test_subset_sum_possible():
    assert subset_sum_possible([3, 1, 4, 2], 6) == "Yes"  # 4+2=6
    assert subset_sum_possible([3, 1, 4], 8) == "Yes"     # 3+1+4=8
    assert subset_sum_possible([3, 1, 4], 9) == "No"      # 最大でも8なので不可能


def test_min_merge_cost():
    assert min_merge_cost([1, 2, 3]) == 9
    assert min_merge_cost([5]) == 0


# ── graph ──
def test_components():
    assert count_components(5, [(0, 1), (1, 2), (3, 4)]) == 2
    assert count_components(3, []) == 3


def test_shortest_steps():
    assert shortest_steps(4, [(0, 1), (1, 2), (2, 3), (0, 3)], 0, 2) == 2
    assert shortest_steps(3, [(0, 1)], 0, 2) == -1


def test_maze():
    assert maze_shortest(["S.", ".G"]) == 2
    assert maze_shortest(["S#", "#G"]) == -1


# ── dijkstra / unionfind ──
def test_dijkstra():
    assert dijkstra(4, [(0, 1, 1), (1, 2, 5), (0, 2, 2), (2, 3, 1)], 0, 3) == 3
    assert dijkstra(2, [], 0, 1) == -1


def test_unionfind():
    uf = UnionFind(4)
    uf.union(0, 1)
    uf.union(1, 2)
    assert uf.same(0, 2) is True
    assert uf.same(0, 3) is False
    assert uf.group_size(0) == 3


def test_friends():
    assert friends_same_group(4, [(0, 1), (1, 2)], [(0, 2), (0, 3)]) == ["Yes", "No"]


# ── greedy / math ──
def test_scheduling():
    assert max_non_overlap([(0, 2), (1, 3), (2, 4)]) == 2
    assert max_non_overlap([(0, 5), (1, 2), (2, 3)]) == 2


def test_lcm():
    assert lcm_of_list([4, 6]) == 12
    assert lcm_of_list([2, 3, 4]) == 12


def test_primes():
    assert primes_upto(10) == [2, 3, 5, 7]
    assert primes_upto(1) == []


def test_modpow():
    assert mod_pow(2, 10, 1000) == 24
    assert mod_pow(3, 0, 7) == 1
    assert mod_pow(7, 100, 13) == pow(7, 100, 13)   # 標準pow と一致
