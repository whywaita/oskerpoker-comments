import datastore


def become_open_flop(elapsed_time_ms: float):
    datastore.set_now_status(datastore.Status.OPEN_FLOP)
    datastore.set_open_flop_time(elapsed_time_ms)


def next_game():
    datastore.reset_store_data()