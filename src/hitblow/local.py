"""ローカル対人戦（2人対戦）モード。

責務は core.py の judge / make_secret を使って
「共通の秘密の数字を2人が交互に当て合う」進行のみ。
1機能=1ファイルの方針に沿って、既存の game.py には手を入れずに独立させている。
"""

from .core import judge, make_secret


def play_versus(digits=3):
    """2人対戦（レース）モード。共通の秘密の数字を先に当てた方が勝ち。"""
    secret = make_secret(digits)
    print(f"ローカル対戦モード（{digits} 桁・重複なし）")
    print("2人で交互に同じ秘密の数字を当て合います。先に当てた方の勝ち！\n")

    name1 = input("プレイヤー1の名前 > ").strip() or "プレイヤー1"
    name2 = input("プレイヤー2の名前 > ").strip() or "プレイヤー2"

    players = [
        {"name": name1, "tries": 0, "hint_offered": False},
        {"name": name2, "tries": 0, "hint_offered": False},
    ]

    turn = 0
    while True:
        current = players[turn % 2]
        opponent = players[(turn + 1) % 2]

        # ===== ヒント機能（相手に見えないよう画面を隠す） =====
        from .hint import offer_hint
        if current["tries"] == 4 and not current["hint_offered"]:
            current["hint_offered"] = True

            print(f"\n{opponent['name']} さんは画面を見ないでください。")
            input(f"{current['name']} さんの番です。準備ができたらEnterを押してください > ")
            print("\n" * 30)  # 前の画面(相手の予想など)を隠す

            offer_hint(secret)

            input("\n確認したらEnterを押してください（見終わったら画面を隠します）> ")
            print("\n" * 30)  # ヒントの内容を隠す

        guess = input(f"\n{current['name']} さんの予想 > ").strip()
        if len(guess) != digits or not guess.isdigit():
            print(f"{digits} 桁の数字で入力してね")
            continue

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