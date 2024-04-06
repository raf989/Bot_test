from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html

from db import queries
from bot import methods

app = FastAPI()


@app.get("/")
def read_docs():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="swagger")


@app.post("/start", status_code=201)
def start(data=Body(example={"start_number": 0})):
    pid = methods.start_bot(data.get("start_number"))
    return {"bot_id": pid}


@app.get("/stop/{bot_id}", status_code=204)
def stop(bot_id: int):
    if not methods.stop_bot(bot_id):
        return JSONResponse({"result": f"Bot {bot_id} is not found."}, status_code=404)


@app.get("/active_bots")
def active_bots():
    return JSONResponse({"active_bots": methods.get_active_bot_list()})


@app.get("/bots_history")
def bots_history():
    result = list()
    bots_records = queries.get_all_bots()
    for bot_record in bots_records:
        result.append(bot_record.serialize())
    return result


@app.on_event("shutdown")
def shutdown_event():
    for pid in methods.get_active_bot_list():
        methods.stop_bot(pid)
