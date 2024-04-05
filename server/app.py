import sys
import subprocess
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse

app = FastAPI()

bots = dict()


@app.post("/start", status_code=201)
def read_root(data=Body()):
    args = [sys.executable, 'bot/bot.py']
    if "start_number" in data:
        args.append(str(data["start_number"]))
    proc = subprocess.Popen(args)
    bots[proc.pid] = proc
    return {"bot_id": proc.pid}


@app.get("/stop/{bot_id}", status_code=204)
def read_root(bot_id: int):
    if bot_id not in bots:
        return JSONResponse({"result": f"Bot {bot_id} is not found."}, status_code=404)
    bots.pop(bot_id).kill()


@app.get("/bots")
def read_root():
    return JSONResponse({"active_bots": list(bots.keys())})
