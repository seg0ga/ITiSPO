import json
from concurrent import futures
from datetime import datetime, timezone

import grpc

notifications=[]
notification_counter=1


def notify_log_created(request_bytes:bytes,context: grpc.ServicerContext)->bytes:
    global notification_counter
    payload=json.loads(request_bytes.decode("utf-8"))
    log_id=payload.get("id")
    level=payload.get("level")
    message=payload.get("message")
    notification={
        "id":notification_counter,
        "log_id":str(log_id),
        "level":level,
        "message":message,
        "received_at":datetime.now(timezone.utc).isoformat(),}
    notifications.append(notification)
    notification_counter+=1
    print(f"received log id={log_id} level={level} message={message}", flush=True)
    response={"ok": True, "status": "notification accepted", "stored": True}
    return json.dumps(response).encode("utf-8")


def get_notifications(request_bytes:bytes,context: grpc.ServicerContext)->bytes:
    payload={}
    if request_bytes:payload=json.loads(request_bytes.decode("utf-8"))
    limit=payload.get("limit")
    items=notifications
    if isinstance(limit,int) and limit>0:items=notifications[-limit:]
    response={"ok":True,"total":len(notifications),"notifications":items,}
    return json.dumps(response).encode("utf-8")

def serve()->None:
    server=grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    handler=grpc.method_handlers_generic_handler(
        "logs.v1.LogsService",{
            "NotifyLogCreated":grpc.unary_unary_rpc_method_handler(notify_log_created,
                request_deserializer=lambda value:value,
                response_serializer=lambda value:value,),
            "GetNotifications":grpc.unary_unary_rpc_method_handler(get_notifications,
                request_deserializer=lambda value:value,
                response_serializer=lambda value:value,)},)
    server.add_generic_rpc_handlers((handler,))
    server.add_insecure_port("[::]:50051")
    server.start()
    print("log-notifier запущен на порту 50051", flush=True)
    server.wait_for_termination()

if __name__ == "__main__":serve()