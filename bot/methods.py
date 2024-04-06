from datetime import datetime
import sys
import subprocess

from db import queries

bots = dict()


def start_bot(start_number=None):
    args = [sys.executable, 'bot/bot.py']
    if start_number is not None:
        args.append(str(start_number))
    proc = subprocess.Popen(args)
    bots[proc.pid] = proc

    queries.new_bot(proc.pid,
                    start_number if start_number is not None else 0,
                    datetime.now())

    return proc.pid


def stop_bot(pid):
    if pid not in bots:
        return False

    bots.pop(pid).kill()

    bot_record = queries.get_bot(pid)
    bot_record.end = datetime.now()
    bot_record.save()

    return True


def get_active_bot_list():
    return list(bots.keys())
