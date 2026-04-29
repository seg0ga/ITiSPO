import json
import os
from collections import Counter

import grpc
from fastapi import FastAPI, HTTPException

from schemas import Log, LogCreate

app=FastAPI(title="logs-s05")

logs_db=[]
id_counter=1
grpc_target=os.getenv("NOTIFIER_GRPC_TARGET","log-notifier:50051")
grpc_method="/logs.v1.LogsService/NotifyLogCreated"

def notify_log_created(log: Log)->dict:
    payload=json.dumps(log.model_dump()).encode("utf-8")

    try:
        with grpc.insecure_channel(grpc_target) as channel:
            stub=channel.unary_unary(
                grpc_method,
                request_serializer=lambda value:value,
                response_deserializer=lambda value:json.loads(value.decode("utf-8")),)
            return stub(payload,timeout=2)
    except Exception:return {"ok":False,"status":"notifier unavailable"}


@app.get("/health")
async def health()->dict:
    return {"status":"ok","project":"logs-s05"}

@app.post("/logs/",response_model=Log,status_code=201)
async def create_log(log:LogCreate)->Log:
    global id_counter

    new_log=Log(id=id_counter,**log.model_dump())
    logs_db.append(new_log)
    id_counter+=1
    notify_log_created(new_log)
    return new_log


@app.get("/logs/",response_model=list[Log])
async def get_logs()->list[Log]:return logs_db


@app.get("/logs/summary")
async def get_summary()->dict:
    counter=Counter(item.level for item in logs_db)
    return {"total":len(logs_db),"by_level":dict(counter)}


@app.get("/logs/{log_id}",response_model=Log)
async def get_log(log_id:int)->Log:
    for item in logs_db:
        if item.id==log_id:return item
    raise HTTPException(status_code=404,detail="Log not found")