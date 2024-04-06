from datetime import datetime
import sys
import subprocess

import psutil
import redis

from db import queries

redis_connection = redis.Redis(host='redis', port=6379, db=0)


def start_bot(start_number=None):
    args = [sys.executable, 'bot/bot.py']
    if start_number is not None:
        args.append(str(start_number))
    proc = subprocess.Popen(args)
    redis_connection.lpush("procs", proc.pid)

    queries.new_bot(proc.pid,
                    start_number if start_number is not None else 0,
                    datetime.now())

    return proc.pid


def stop_bot(pid):
    if redis_connection.lrem("procs", 1, pid) == 0:
        return False

    psutil.Process(pid).kill()

    bot_record = queries.get_bot(pid)
    bot_record.end = datetime.now()
    bot_record.save()

    return True


def get_active_bot_list():
    length = redis_connection.llen("procs")
    if length == 0:
        return []
    return [int(pid) for pid in redis_connection.lrange("procs", 0, length - 1)]
