
import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds


class DefaultBoard():
    def __init__(self, board_config: dict = {}):
        self.board_name = board_config.get('name', '')
        self.board_config = board_config.get('board_config', {})
        self.board = None

    def _logger(self, message):
        return BoardShim.log_message(LogLevels.LEVEL_INFO.value, message)

    def establish_session(self):
        params = BrainFlowInputParams()
        board = BoardShim(BoardIds.SYNTHETIC_BOARD.value, params)
        self._logger('Board is initialized.')
        if not board.is_prepared():
            board.prepare_session()
            self._logger('Session with the board is established.')

        self.board = board

    def start_streaming(self):
        self._logger(f'Data from {self.board_name} is online!')
        self.board.start_stream()

    def stop_streaming(self):
        self._logger(f'Device {self.board_name} is stopping streaming data!')
        self.board.stop_stream()

    def release_session(self):
        self._logger(f'Device {self.board_name} is releasing session!')
        self.board.release_session()