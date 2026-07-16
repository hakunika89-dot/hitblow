"""ローカル対人戦（2人対戦）モード。

責務は core.py の judge を使って「2人が交互に相手の秘密を当てる」進行のみ。
1機能=1ファイルの方針に沿って、既存の game.py には手を入れずに独立させている。
"""

import getpass

from .core import judge


def _input_secret(player_name, digits):
    """指定プレイヤーの秘密の数字を非表示で受け取る（重複なし digits 桁）。"""
    while True:
        secret = getpass.getpass(
            f"{player_name} さん、{digits} 桁の秘密の数字を入力（非表示）> "
        ).strip()
        if len(secret) == digits and secret.isdigit() and len(set(secret)) == digits:
            return secret
        print(f"{digits} 桁・重複なしの数字で入力してね")


def play_versus(digits=3):
    """2人対戦モード。先に相手の秘密を当てた方が勝ち。"""
    print(f"ローカル対戦モード（{digits} 桁・重複なし）")
    print("それぞれ秘密の数字を設定してから、交互に相手の数字を当てます\n")

    name1 = input("プレイヤー1の名前 > ").strip() or "プレイヤー1"
    name2 = input("プレイヤー2の名前 > ").strip() or "プレイヤー2"

    print(f"\n{name1} さんの番です。{name2} さんは画面を見ないでください。")
    secret1 = _input_secret(name1, digits)
    print("\n" * 30)  # 画面をスクロールして前の入力を隠す

    print(f"{name2} さんの番です。{name1} さんは画面を見ないでください。")
    secret2 = _input_secret(name2, digits)
    print("\n" * 30)

    players = [
        {"name": name1, "target": secret2, "tries": 0},
        {"name": name2, "target": secret1, "tries": 0},
    ]

    turn = 0
    while True:
        current = players[turn % 2]
        other_name = players[(turn + 1) % 2]["name"]

        guess = input(f"\n{current['name']} さんの予想（{other_name} さんの数字）> ").strip()
        if len(guess) != digits or not guess.isdigit():
            print(f"{digits} 桁の数字で入力してね")
            continue

        current["tries"] += 1
        hit, blow = judge(current["target"], guess)
        print(f"  Hit={hit}  Blow={blow}")

        if hit == digits:
            print(
                f"\n🎉 {current['name']} さんの勝ち！ "
                f"{current['tries']} 回で当てました（答え {current['target']}）"
            )
            break

        turn += 1