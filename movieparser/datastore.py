import enum
import typing


class Status(enum.Enum):
    PRE_FLOP = 'PRE_FLOP'
    OPEN_FLOP = 'OPEN_FLOP'


class FlopTime:
    def __init__(self, time: float, players: typing.List[str]):
        self.time = time
        self.players = players


PLAYERS = []
NOW_STATUS = Status.PRE_FLOP
FOUND_TIME = str()
OPEN_FLOP_TIME = float()


def reset_store_data():
    global NOW_STATUS  # pylint: disable=global-statement
    global PLAYERS  # pylint: disable=global-statement
    global FOUND_TIME  # pylint: disable=global-statement
    NOW_STATUS = Status.PRE_FLOP
    PLAYERS = []
    FOUND_TIME = str()


# def detect_now_status(frame_data: cv2.Mat) -> str:
#     if cv.is_open_flop(frame_data):
#         return 'OPEN_FLOP'
#     return 'PRE_FLOP'

def set_now_status(status: Status):
    global NOW_STATUS  # pylint: disable=global-statement
    NOW_STATUS = status


def get_now_status() -> Status:
    return NOW_STATUS


def add_player(player_name: str):
    global PLAYERS  # pylint: disable=global-variable-not-assigned
    if player_name not in PLAYERS:
        PLAYERS.append(player_name)


def get_players() -> list:
    return PLAYERS


def set_open_flop_time(time: float):
    global OPEN_FLOP_TIME  # pylint: disable=global-statement
    OPEN_FLOP_TIME = time


def get_open_flop_time() -> float:
    return OPEN_FLOP_TIME
