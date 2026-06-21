"""AtCoder 緑コーダー — 典型アルゴリズム問題集。

緑(レート800-1200)で「ほぼ確実に解けるべき」典型テーマを、
自作問題＋模範解＋テストのセットで学ぶ。各テーマは独立して動く。

収録テーマ:
  full_search          … 全探索 / bit全探索
  binary_search        … 二分探索 / めぐる式 / 答えで二分
  cumulative_sum       … 累積和 / いもす法
  dp                   … ナップサック / LIS / 区間DP / 部分和
  graph                … BFS / DFS / 連結成分 / 最短路(BFS)
  dijkstra_unionfind   … ダイクストラ / Union-Find(DSU)
  greedy_math          … 貪欲 / GCD・LCM / エラトステネスの篩 / 繰り返し二乗法

各モジュールは `python -m atcoder_training.dp` のように実行でき、
内蔵の入出力例で答え合わせ(self-check)が走る。
"""
