"""ローカル対人戦（2人対戦）モード。

責務は core.py の judge / make_secret を使って
「共通の秘密の数字を2人が交互に当て合う」進行のみ。
1機能=1ファイルの方針に沿って、既存の game.py には手を入れずに独立させている。
"""

import sys

from .core import judge, make_secret

try:
    import msvcrt  # Windows
    _IS_WINDOWS = True
except ImportError:
    import termios  # macOS / Linux
    import tty
    _IS_WINDOWS = False


def _read_masked_input(digits):
    """1文字ずつ読み取り、入力するたびに * を表示する（改行なし）。

    - 数字のみ受け付け、指定 digits 桁に達したら自動で確定
    - Backspace で1文字消せる
    """
    buf = []

    if _IS_WINDOWS:
        while len(buf) < digits:
            ch = msvcrt.getwch()
            if ch in ("\b",):  # Backspace
                if buf:
                    buf.pop()
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
            elif ch.isdigit():
                buf.append(ch)
                sys.stdout.write("*")
                sys.stdout.flush()
        print()  # 改行
        return "".join(buf)

    # macOS / Linux
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        while len(buf) < digits:
            ch = sys.stdin.read(1)
            if ch in ("\x7f", "\b"):  # Backspace (多くの端末では 0x7f)
                if buf:
                    buf.pop()
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
            elif ch.isdigit():
                buf.append(ch)
                sys.stdout.write("*")
                sys.stdout.flush()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    print()  # 改行
    return "".join(buf)


def _input_guess(player_name, digits):
    """指定プレイヤーの予想を * でマスクしながら受け取る（digits 桁の数字）。"""
    print(f"{player_name} さんの予想 > ", end="", flush=True)
    return _read_masked_input(digits)


def play_versus(digits=3):
    """2人対戦（レース）モード。共通の秘密の数字を先に当てた方が勝ち。"""
    secret = make_secret(digits)
    print(f"ローカル対戦モード（{digits} 桁・重複なし）")
    print("2人で交互に同じ秘密の数字を当て合います。先に当てた方の勝ち！")
    print(f"予想は * で表示されます（{digits} 桁入力すると自動で確定）\n")

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