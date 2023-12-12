from random import choice, randint

from nim_game.common.enumerations import AgentLevels
from nim_game.common.models import NimStateChange


def validate_level(level: str) -> AgentLevels:
    """
    Возвращает элемент AgentLevels или поднимает ValueError
    """

    if level == AgentLevels.EASY.value:
        return AgentLevels.EASY
    elif level == AgentLevels.NORMAL.value:
        return AgentLevels.NORMAL
    elif level == AgentLevels.HARD.value:
        return AgentLevels.HARD
    else:
        raise ValueError("Unknown value of level")


class Agent:
    """
    В этом классе реализованы стратегии игры для уровней сложности
    """

    _level: AgentLevels         # уровень сложности

    def __init__(self, level: str) -> None:
        self._level = validate_level(level)

    def make_step(self, state_curr: list[int]) -> NimStateChange:
        """
        Сделать шаг, соответствующий уровню сложности

        :param state_curr: список целых чисел - состояние кучек
        :return: структуру NimStateChange - описание хода
        """

        if self._level == AgentLevels.EASY:
            return self._make_dull_move(state_curr)
        elif self._level == AgentLevels.HARD:
            return self._make_smart_move(state_curr)
        else:
            if randint(0, 1):
                return self._make_dull_move(state_curr)
            else:
                return self._make_smart_move(state_curr)

    def _make_smart_move(self, state_curr: list[int]) -> NimStateChange:
        """
        Делает ход так, чтобы Ним-сумма оставалась нулевой, иначе берёт один
        камень из первой ненулевой кучи
        """

        max_ = 1
        imax = 0
        for i in range(len(state_curr)):
            if state_curr[i] != 0:
                imax = i
                break

        for i in range(imax, len(state_curr)):
            for j in range(1, state_curr[i] + 1):
                state_curr[i] -= j

                if self.nim_sum(state_curr) == 0:
                    max_ = max(max_, j)
                    imax = max(imax, i)

                state_curr[i] += j

        return NimStateChange(
            heap_id=imax + 1,
            decrease=max_
        )

    def _make_dull_move(self, state_curr: list[int]) -> NimStateChange:
        """
        Берёт случайное количество камней из случайной ненулевой кучи
        """

        heap_num = choice(
            [i for i in range(len(state_curr)) if state_curr[i] != 0]
        )
        things_num = randint(1, state_curr[heap_num])

        return NimStateChange(
            heap_id=heap_num + 1,
            decrease=things_num
        )

    def nim_sum(self, state_curr: list[int]) -> int:
        """
        Возвращает Ним-сумму кучек
        """

        res = state_curr[0]
        for i in range(1, len(state_curr)):
            res ^= state_curr[i]

        return res
