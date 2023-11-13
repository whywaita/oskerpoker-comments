import enum


class Status(enum.Enum):
    PRE_FLOP = 'PRE_FLOP'
    OPEN_FLOP = 'OPEN_FLOP'


PLAYERS = list()
NOW_STATUS = Status.PRE_FLOP
FOUND_TIME = str()
OPEN_FLOP_TIME = float()


def reset_store_data():
    global NOW_STATUS
    global PLAYERS
    global FOUND_TIME
    NOW_STATUS = Status.PRE_FLOP
    PLAYERS = list()
    FOUND_TIME = str()


# def detect_now_status(frame_data: cv2.Mat) -> str:
#     if cv.is_open_flop(frame_data):
#         return 'OPEN_FLOP'
#     return 'PRE_FLOP'

def set_now_status(status: Status):
    global NOW_STATUS
    NOW_STATUS = status


def get_now_status() -> str:
    global NOW_STATUS
    return NOW_STATUS


def add_player(player_name: str):
    global PLAYERS
    if player_name not in PLAYERS:
        PLAYERS.append(player_name)


def get_players() -> list:
    global PLAYERS
    return PLAYERS


def set_open_flop_time(time: float):
    global OPEN_FLOP_TIME
    OPEN_FLOP_TIME = time


def get_open_flop_time() -> float:
    global OPEN_FLOP_TIME
    return OPEN_FLOP_TIME