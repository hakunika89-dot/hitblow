"""コマンドの入口。第3回で `hitblow` コマンドがここ（main）を呼ぶ。"""

from .game import play
from .local import play_versus
from .bomb import play_bomb_mode

def main():
    modes = {
        "1": {
            "name": "CPU対戦",
            "function": play
        },
        "2": {
            "name": "2人対戦",
            "function": play_versus
        },
        "3":{
            "name":"地雷モード",
            "function":play_bomb_mode
        }
    }

    print("=== モード選択 ===")

    for number, mode in modes.items():
        print(f"{number}. {mode['name']}")

    while True:
        selected = input("モード番号を選択してください：")

        if selected in modes:
            selected_mode = modes[selected]

            print(f"{selected_mode['name']}を開始します。")
            selected_mode["function"]()
            break

        print("正しいモード番号を入力してください。")


if __name__ == "__main__":
    main()