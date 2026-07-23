"""ヒント（救済）機能。

5回目の挑戦の直前に一度だけ、正解の数字を1桁「位置つき」で教えるか尋ねる。
使っても使わなくても、以降は二度と使えない（1ゲームにつき1回だけの判定）。
"""

import random


def offer_hint(secret):
    """5回目の挑戦の直前に呼ぶ。使うか尋ね、使うなら「何桁目が何の数字か」を教える。

    呼び出し側は「もう聞いたかどうか」を管理し、この関数は一度だけ呼ぶこと。
    """
    answer = input(
        "\nヒント：プライドを捨てますか（使用できるのは今回限りです） (y/n) > "
    ).strip().lower()

    if answer in ("y", "yes", "はい"):
        position = random.randrange(len(secret))
        digit = secret[position]
        print(f"ヒント: 正解の{position + 1}桁目は「{digit}」です\n")
    else:
        print("草\n")