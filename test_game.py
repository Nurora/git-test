"""game.py 的 pytest 测试。

重点验证游戏逻辑（比较、范围、循环收敛），不依赖真实键盘输入。
"""

import pytest

from game import check_guess, generate_secret, play


# ---------- 1. 比较逻辑 ----------
def test_check_guess_low():
    assert check_guess(3, 10) == "low"


def test_check_guess_high():
    assert check_guess(15, 10) == "high"


def test_check_guess_correct():
    assert check_guess(10, 10) == "correct"


def test_check_guess_boundary():
    # 边界值：恰好在目标两侧
    assert check_guess(9, 10) == "low"
    assert check_guess(11, 10) == "high"


# ---------- 2. 答案生成 ----------
def test_generate_secret_in_range():
    for _ in range(1000):
        s = generate_secret(1, 100)
        assert 1 <= s <= 100


def test_generate_secret_single_value():
    # 区间退化为一个点时，只能返回该点
    assert generate_secret(42, 42) == 42


def test_generate_secret_invalid_range():
    with pytest.raises(ValueError):
        generate_secret(100, 1)


# ---------- 3. 游戏循环（用 monkeypatch 驱动输入） ----------
def test_play_converges(monkeypatch):
    """固定答案为 42，模拟依次猜 10、90、42，应在第 3 次猜中。"""
    import game

    monkeypatch.setattr(game, "generate_secret", lambda *a, **k: 42)
    inputs = iter(["10", "90", "42"])
    monkeypatch.setattr("builtins.input", lambda *a, **k: next(inputs))

    attempts = play()
    assert attempts == 3


def test_play_skips_invalid_then_wins(monkeypatch):
    """非法输入不应计入次数，且最终能收敛。"""
    import game

    monkeypatch.setattr(game, "generate_secret", lambda *a, **k: 7)
    inputs = iter(["abc", "7"])  # 先输一个非数字
    monkeypatch.setattr("builtins.input", lambda *a, **k: next(inputs))

    attempts = play()
    assert attempts == 1
