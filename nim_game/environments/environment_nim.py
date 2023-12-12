from random import randint

from nim_game.common.models import NimStateChange


STONE_AMOUNT_MIN = 1        # минимальное начальное число камней в кучке
STONE_AMOUNT_MAX = 10       # максимальное начальное число камней в кучке


def validate_heaps_amount(heaps_amount) -> int:
    """
    Возвращает int или поднимает ValueError
    """

    if 2 <= heaps_amount <= 10:
        return heaps_amount

    raise ValueError("Amount of heaps must be in diapason from 2 to 10")


class EnvironmentNim:
    """
    Класс для хранения и взаимодействия с кучками
    """

    _heaps: list[int]       # кучки

    def __init__(self, heaps_amount: int) -> None:
        self._heaps_amount = validate_heaps_amount(heaps_amount)
        self._heaps = [randint(STONE_AMOUNT_MIN, STONE_AMOUNT_MAX) for _ in range(heaps_amount)]

    def get_state(self) -> list[int]:
        """
        Получение текущего состояния кучек

        :return: копия списка с кучек
        """

        return self._heaps

    def change_state(self, state_change: NimStateChange) -> None:
        """
        Изменения текущего состояния кучек

        :param state_change: структура описывающая изменение состояния
        """

        self._validate_NimStateChange(state_change)
        self._heaps[state_change.heap_id - 1] -= state_change.decrease

    def _validate_NimStateChange(self, state_change: NimStateChange) -> None:
        if (
            state_change.heap_id < 1 or
            state_change.heap_id > self._heaps_amount
        ):
            raise ValueError(
                "NimStateChanges.heap_id must be "
                "in diapason from 1 to heaps_amount"
                f"{state_change.heap_id, self._heaps_amount}"
            )

        if (
            state_change.decrease < 1 or
            state_change.decrease > self._heaps[state_change.heap_id - 1]
        ):
            raise ValueError(
                "NimStateChanges.decrease must be in diapason from 1 "
                "to number of stones in current heap"
                f"{state_change.decrease, state_change.heap_id, self._heaps[state_change.heap_id]}\n"
                f"{self.get_state()}"
            )
