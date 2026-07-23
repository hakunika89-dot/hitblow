"""地雷（ボム）モード・完全一致版。

正解とは別に「地雷ナンバー（3桁）」が設定されます。
予想が地雷ナンバーと「完全一致」した場合のみ即ゲームオーバーです。
運ゲーを防ぐため、地雷ナンバーに近い入力をすると警告が出ます。
"""

from .core import judge, make_secret

def play_bomb_mode(digits=3):
    """地雷モードのメインループ（3桁・完全一致型）"""
    print(f"💣 地雷モード（{digits} 桁・重複なし） 💣")
    print("【ルール】")
    print("1. 正解とは別に、秘密の「地雷ナンバー」が1つ隠されています。")
    print("2. 予想が地雷ナンバーと「完全一致」すると大爆発（ゲームオーバー）！")

    # 答えの数字を生成
    secret = make_secret(digits)

    # 10個の地雷ナンバーを生成（答えと被らず，地雷同士も被らないようにする）
    bomb_numbers = []
    while len(bomb_numbers) < 10:
        bomb = make_secret(digits)
        if bomb != secret and bomb not in bomb_numbers:
            bomb_numbers.append(bomb)

    tries = 0
    while True:
        guess = input("\n予想を入力 > ").strip()

        # 入力チェック
        if len(guess) != digits or not guess.isdigit():
            print(f"{digits} 桁の数字で入力してください。")
            continue

        tries += 1

        # 【追加】地雷との完全一致判定
        if guess in bomb_numbers:
            print("\n💥 ドカーン！！ 💥")
            print(f"地雷ナンバー「{guess}」を完全に入力してしまいました！")
            print(f"即ゲームオーバーです。正解は {secret} でした。（{tries} 回目で爆死）")
            break
        

        # 通常のHit & Blow判定
        hit, blow = judge(secret, guess)
        print(f"  Hit={hit}  Blow={blow}")

        # クリア判定
        if hit == digits:
            print(f"\n🎉 クリア！ {tries} 回で当てました！（答え {secret}）")
            print("見事に地雷を回避しながら正解を導き出しましたね。")
            break

# パッケージ実行用の起動設定
if __name__ == "__main__":
    play_bomb_mode()
