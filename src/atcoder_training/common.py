"""共通の小道具。各テーマの「入出力例で答え合わせ」を見やすくするだけ。

■ なぜ self-check 方式にする？
  AtCoder では「サンプル入出力」が必ず与えられる。まずそれに通すのが基本。
  各問題の模範解に、サンプルを使った確認(check)を付けておけば、
  `python -m atcoder_training.dp` を実行するだけで「合ってる/間違ってる」が分かる。
"""

from __future__ import annotations

from typing import Any, Callable


def check(name: str, got: Any, expected: Any) -> bool:
    """1ケース答え合わせして、結果を1行表示する。

    got(自分の答え) と expected(正解) が同じなら OK、違えば NG を出す。
    """
    ok = got == expected
    mark = "✅" if ok else "❌"
    print(f"  {mark} {name}: got={got!r} expected={expected!r}")
    return ok


def run_cases(title: str, cases: list[tuple[str, Callable[[], Any], Any]]) -> None:
    """同じテーマの複数ケースをまとめて流す。

    cases は (ケース名, 答えを返す関数, 正解) のリスト。
    """
    print(f"=== {title} ===")
    all_ok = True
    for name, fn, expected in cases:
        all_ok &= check(name, fn(), expected)
    print(f"  → {'全ケースOK' if all_ok else '失敗あり'}\n")
