"""简单的猜数字小游戏。

核心逻辑（check_guess / generate_secret）与交互（play）分离，
便于用 pytest 直接测试游戏逻辑，无需真实键盘输入。
"""

import random


def generate_secret(min_val: int = 1, max_val: int = 100) -> int:
    """生成一个 [min_val, max_val] 区间内的随机整数作为答案。"""
    if min_val > max_val:
        raise ValueError("min_val 必须小于或等于 max_val")
    return random.randint(min_val, max_val)


def check_guess(guess: int, secret: int) -> str:
    """比较一次猜测与答案，返回 'low' / 'high' / 'correct'。"""
    if guess < secret:
        return "low"
    if guess > secret:
        return "high"
    return "correct"


def play(min_val: int = 1, max_val: int = 100) -> int:
    """运行交互式猜数字游戏，返回猜中所需的次数。"""
    secret = generate_secret(min_val, max_val)
    attempts = 0
    print(f"我想了一个 {min_val} 到 {max_val} 之间的整数，猜猜看？")
    while True:
        try:
            guess = int(input("请输入你的猜测: "))
        except ValueError:
            print("请输入一个有效的整数。")
            continue
        attempts += 1
        result = check_guess(guess, secret)
        if result == "low":
            print("太小了！")
        elif result == "high":
            print("太大了！")
        else:
            print(f"恭喜，猜对了！你一共用了 {attempts} 次。")
            return attempts


if __name__ == "__main__":
    play()
