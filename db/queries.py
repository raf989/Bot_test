from db.models import *


def get_bot(pid):
    return session.query(Bot).filter_by(pid=pid).first()


def get_all_bots():
    return session.query(Bot).filter_by().all()


def new_bot(pid, start_number, start, end=None):
    bot = get_bot(pid)
    if bot is None:
        bot = Bot(
            pid=pid,
            start_number=start_number,
            start=start,
            end=end,
        )
        bot.save()
    return bot
