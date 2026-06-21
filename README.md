# atcoder-green-training — AtCoder 緑コーダー 問題集

緑(レート 800〜1200)で「ほぼ確実に解けるべき」典型アルゴリズムを、
**自作問題＋模範解＋テスト**のセットで身につける学習用リポジトリ。
本番の問題は転載せず、各テーマの典型を自作問題に落とし込んでいる。

## 構成（src/atcoder_training/）

| モジュール | テーマ | 収録問題 |
|---|---|---|
| `full_search.py` | 全探索 / bit全探索 | ぴったりの組・部分集合の和・サイコロの積 |
| `binary_search.py` | 二分探索 / めぐる式 / 答えで二分 | lower_bound・値の個数・最大の棒の長さ |
| `cumulative_sum.py` | 累積和 / いもす法 / 2次元累積和 | 区間和・重なり回数・長方形和 |
| `dp.py` | DP | 0-1ナップサック・LIS・部分和・区間DP |
| `graph.py` | BFS / DFS / 連結成分 | 島の数・最短手数・迷路最短 |
| `dijkstra_unionfind.py` | ダイクストラ / Union-Find | 重み付き最短・グループ判定 |
| `greedy_math.py` | 貪欲 / 数学 | 区間スケジューリング・LCM・素数列挙・modpow |

各モジュールは単体で実行でき、内蔵のサンプル入出力で答え合わせが走る:

```bash
arch -arm64 python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=src

python -m atcoder_training.dp          # 例: DP の各問題を self-check
pytest                                  # 全テーマをまとめて検証
```

## 計算量 早見表（緑で必須の感覚）

| データ規模 N | 間に合う手法 |
|---|---|
| N ≤ 10 | 2^N の bit全探索 |
| N ≤ 2000 | O(N^2) 二重ループ |
| N ≤ 10^5〜10^6 | O(N log N)（ソート・二分探索・累積和・ダイクストラ・DP） |
| 巨大な指数 | 繰り返し二乗法 O(log b) |

## テスト
7テーマ・全模範解を **pytest 23件 全green**（各問題をサンプル入出力とエッジケースで検証）。

## 学習の使い方
1. 各ファイル冒頭の「たとえ話」と「計算量の感覚」を読む。
2. 模範解のコメント（なぜこの遷移か・なぜ逆順ループか 等）を追う。
3. `python -m atcoder_training.<テーマ>` で動かして出力を確認する。

---
> 📝 学習目的の自己完結プロジェクトです（合成データで動く再実装）。AIコーディング支援を活用して実装し、設計・各処理を自分の言葉で説明できる状態にした上で公開しています。研究成果ではなく学習用です。
