import time
import requests
import grpc
import service_pb2
import service_pb2_grpc

def run_rest_bench():
    print("Запуск REST бэнчмарка...")
    start = time.time()
    for _ in range(1000):
        requests.get("http://localhost:8080/products/")
    end = time.time()
    print(f"REST: {end - start:.4f} сек")

def run_grpc_bench():
    print("Запуск gRPC бэнчмарка...")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.PhotosServiceStub(channel)
        start = time.time()
        for _ in range(1000):
            stub.GetPhoto(service_pb2.PhotoRequest(id="1"))
        end = time.time()
        print(f"gRPC: {end - start:.4f} сек")

def test_streaming():
    print("\nТест streaming метода...")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.PhotosServiceStub(channel)
        request = service_pb2.SubscribeRequest(ids=["1", "2", "3"])
        count=0
        for update in stub.SubscribePhotos(request):count+=1
        print(f"Streaming завершен, получено {count} обновлений")

if __name__ == "__main__":
    run_rest_bench()
    run_grpc_bench()
    test_streaming()