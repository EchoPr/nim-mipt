import json

from nim_game.environments.environment_nim import EnvironmentNim
from nim_game.common.models import NimStateChange, GameState
from nim_game.agents.agent import Agent
from nim_game.common.enumerations import Players


def load_json(path: str) -> dict:
    """
    Выгружает данные о конфигурации игры
    """
    try:
        with open(path) as file:
            res = json.load(file)
    except FileNotFoundError:
        raise ValueError("Unknown path to game config")

    return res


class GameNim:
    _environment: EnvironmentNim        # состояния кучек
    _agent: Agent                       # бот

    def __init__(self, path_to_config: str) -> None:
        game_config = load_json(path_to_config)

        self._environment = EnvironmentNim(game_config["heaps_amount"])
        self._agent = Agent(game_config["opponent_level"])

    def make_steps(self, player_step: NimStateChange) -> GameState:
        """
        Изменение среды ходом игрока + ход бота

        :param player_step: изменение состояния кучек игроком
        """

        game_state = GameState()
        opponent_step = None

        self._environment.change_state(player_step)
        if not self.is_game_finished():
            opponent_step = self._agent.make_step(self.heaps_state)

        game_state = GameState(
            opponent_step=opponent_step,
            heaps_state=self.heaps_state,
        )

        if self.is_game_finished():
            game_state.winner = Players.BOT if opponent_step else Players.USER

        return game_state

    def is_game_finished(self) -> bool:
        """
        Проверить, завершилась ли игра, или нет

        :return: True - игра окончена, False - иначе
        """

        return sum(self.heaps_state) == 0

    @property
    def heaps_state(self) -> list[int]:
        return self._environment.get_state()
