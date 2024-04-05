from datetime import datetime
import sys
import subprocess
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from db import queries

app = FastAPI()

bots = dict()


@app.post("/start", status_code=201)
def start(data=Body()):
    args = [sys.executable, 'bot/bot.py']
    if "start_number" in data:
        args.append(str(data["start_number"]))
    proc = subprocess.Popen(args)
    bots[proc.pid] = proc
    queries.new_bot(proc.pid, datetime.now())
    return {"bot_id": proc.pid}


@app.get("/stop/{bot_id}", status_code=204)
def stop(bot_id: int):
    if bot_id not in bots:
        return JSONResponse({"result": f"Bot {bot_id} is not found."}, status_code=404)
    bots.pop(bot_id).kill()
    bot_record = queries.get_bot(bot_id)
    bot_record.end = datetime.now()
    bot_record.save()


@app.get("/active_bots")
def active_bots():
    return JSONResponse({"active_bots": list(bots.keys())})


@app.get("/bots_history")
def bots_history():
    result = list()
    bots_records = queries.get_all_bots()
    for bot_record in bots_records:
        result.append(bot_record.serialize())
    return result
