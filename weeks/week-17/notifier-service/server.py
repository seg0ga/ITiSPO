import json
from concurrent import futures

import grpc


def notify_log_created(request_bytes:bytes,context: grpc.ServicerContext)->bytes:
    payload=json.loads(request_bytes.decode("utf-8"))
    log_id=payload.get("id")
    level=payload.get("level")
    message=payload.get("message")
    print(f"received log id={log_id} level={level} message={message}")
    response={"ok": True, "status": "notification accepted"}
    return json.dumps(response).encode("utf-8")

def serve()->None:
    server=grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    handler=grpc.method_handlers_generic_handler(
        "logs.v1.LogsService",{
            "NotifyLogCreated":grpc.unary_unary_rpc_method_handler(notify_log_created,
                request_deserializer=lambda value:value,
                response_serializer=lambda value:value,)},)
    server.add_generic_rpc_handlers((handler,))
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":serve()