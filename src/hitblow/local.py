"""ローカル対人戦（2人対戦）モード。

責務は core.py の judge / make_secret を使って
「共通の秘密の数字を2人が交互に当て合う」進行のみ。
1機能=1ファイルの方針に沿って、既存の game.py には手を入れずに独立させている。
"""

import getpass

from .core import judge, make_secret


def _input_guess(player_name, digits):
    """指定プレイヤーの予想を非表示で受け取る（digits 桁の数字）。"""
    while True:
        guess = getpass.getpass(f"{player_name} さんの予想（非表示）> ").strip()
        if len(guess) == digits and guess.isdigit():
            return guess
        print(f"{digits} 桁の数字で入力してね")


def play_versus(digits=3):
    """2人対戦（レース）モード。共通の秘密の数字を先に当てた方が勝ち。"""
    secret = make_secret(digits)
    print(f"ローカル対戦モード（{digits} 桁・重複なし）")
    print("2人で交互に同じ秘密の数字を当て合います。先に当てた方の勝ち！")
    print("予想の入力は非表示になります（隣の人に見えません）\n")

    name1 = input("プレイヤー1の名前 > ").strip() or "プレイヤー1"
    name2 = input("プレイヤー2の名前 > ").strip() or "プレイヤー2"

    players = [
        {"name": name1, "tries": 0},
        {"name": name2, "tries": 0},
    ]

    turn = 0
    while True:
        current = players[turn % 2]

        guess = _input_guess(current["name"], digits)
        current["tries"] += 1
        hit, blow = judge(secret, guess)
        print(f"  Hit={hit}  Blow={blow}")

        if hit == digits:
            print(
                f"\n🎉 {current['name']} さんの勝ち！ "
                f"{current['tries']} 回で当てました（答え {secret}）"
            )
            break

        turn += 1