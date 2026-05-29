from concurrent import futures
from datetime import datetime, timezone
import grpc
import logs_pb2
import logs_pb2_grpc

notifications=[]
notification_counter=1


class LogsService(logs_pb2_grpc.LogsServiceServicer):
    def NotifyLogCreated(self,request,context):
        global notification_counter
        log_id=request.id
        level=request.level
        message=request.message
        notification={
            "id":notification_counter,
            "log_id":str(log_id),
            "level":level,
            "message":message,
            "received_at":datetime.now(timezone.utc).isoformat(),}
        notifications.append(notification)
        notification_counter+=1
        print(f"received log id={log_id} level={level} message={message}", flush=True)
        return logs_pb2.NotifyLogResponse(ok=True,status="notification accepted",stored=True)

    def GetNotifications(self,request,context):
        limit=request.limit if request.limit>0 else None
        items=notifications
        if limit is not None:items=notifications[-limit:]
        return logs_pb2.GetNotificationsResponse(
            ok=True,
            total=len(notifications),
            notifications=[
                logs_pb2.Notification(
                    id=item["id"],
                    log_id=item["log_id"],
                    message=item["message"],
                    level=item["level"],
                    received_at=item["received_at"],)
                for item in items],)


def serve()->None:
    server=grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    logs_pb2_grpc.add_LogsServiceServicer_to_server(LogsService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("log-notifier started on port 50051", flush=True)
    server.wait_for_termination()

if __name__ == "__main__":serve()