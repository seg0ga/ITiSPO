import json
import os
import time
from collections import Counter

import grpc
from fastapi import FastAPI, HTTPException, Query

from schemas import Log, LogCreate, LogSummary, NotificationList

app=FastAPI(title="logs-s05")

logs_db=[]
id_counter=1
grpc_target=os.getenv("NOTIFIER_GRPC_TARGET","log-notifier:50051")
grpc_method="/logs.v1.LogsService/NotifyLogCreated"
grpc_notifications_method="/logs.v1.LogsService/GetNotifications"

def notify_log_created(log: Log)->dict:
    payload=json.dumps(log.model_dump()).encode("utf-8")
    for attempt in range(3):
        try:
            with grpc.insecure_channel(grpc_target) as channel:
                stub=channel.unary_unary(
                    grpc_method,
                    request_serializer=lambda value:value,
                    response_deserializer=lambda value:json.loads(value.decode("utf-8")),)
                return stub(payload,timeout=2)
        except Exception:
            if attempt<2:time.sleep(0.2)
    return {"ok":False,"status":"notifier unavailable"}

def get_notifications(limit:int|None=None)->NotificationList:
    request_payload={}
    if limit is not None:
        request_payload["limit"]=limit
    payload=json.dumps(request_payload).encode("utf-8")
    for attempt in range(3):
        try:
            with grpc.insecure_channel(grpc_target) as channel:
                stub=channel.unary_unary(
                    grpc_notifications_method,
                    request_serializer=lambda value:value,
                    response_deserializer=lambda value:json.loads(value.decode("utf-8")),)
                data=stub(payload,timeout=2)
                return NotificationList(**data)
        except Exception:
            if attempt<2:time.sleep(0.2)
    return NotificationList(ok=False,total=0,notifications=[])

def find_log_index(log_id:int)->int:
    for index, item in enumerate(logs_db):
        if item.id==log_id:return index
    return -1

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

@app.get("/logs/summary",response_model=LogSummary)
async def get_summary()->LogSummary:
    counter=Counter(item.level for item in logs_db)
    return LogSummary(total=len(logs_db),by_level=dict(counter))

@app.get("/logs/level/{level}",response_model=list[Log])
async def get_logs_by_level(level:str)->list[Log]:
    normalized=level.casefold()
    return [item for item in logs_db if item.level.casefold()==normalized]

@app.get("/logs/{log_id}",response_model=Log)
async def get_log(log_id:int)->Log:
    for item in logs_db:
        if item.id==log_id:return item
    raise HTTPException(status_code=404,detail="Log not found")

@app.delete("/logs/{log_id}",response_model=Log)
async def delete_log(log_id:int)->Log:
    index=find_log_index(log_id)
    if index<0:raise HTTPException(status_code=404,detail="Log not found")
    deleted_log=logs_db.pop(index)
    return deleted_log


@app.get("/notifications",response_model=NotificationList)
async def proxy_notifications(limit:int|None=Query(default=None,ge=1))->NotificationList:
    return get_notifications(limit)
