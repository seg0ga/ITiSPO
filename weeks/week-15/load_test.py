import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

REST_URL="http://localhost:8208/products/"
DURATION=30
CONNECTIONS=[10,100,1000]

def test_rest(concurrency):
    latencies=[]
    count=[0]
    stop=[False]
    
    def make_request():
        while not stop[0]:
            start=time.time()
            try:
                urllib.request.urlopen(REST_URL,timeout=30)
                latencies.append((time.time()-start)*1000)
                count[0]+=1
            except:pass
    
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures=[executor.submit(make_request) for _ in range(concurrency)]
        time.sleep(DURATION)
        stop[0]=True
        for f in futures:f.result()
    
    latencies.sort()
    rps=count[0]/DURATION
    avg=sum(latencies)/len(latencies) if latencies else 0
    p50=latencies[len(latencies)//2] if latencies else 0
    p95=latencies[int(len(latencies)*0.95)] if latencies else 0
    p99=latencies[int(len(latencies)*0.99)] if latencies else 0
    
    print(f"REST  |{concurrency:>5} |{rps:>8.0f}| {avg:>7.1f} |{p50:>7.1f} |{p95:>7.1f} |{p99:>7.1f} |{count[0]:>6}")

def test_grpc(concurrency):
    import sys
    sys.path.insert(0, '../week-07/starter')
    import grpc
    from service_pb2 import PhotoRequest
    from service_pb2_grpc import PhotosServiceStub
    
    latencies=[]
    count=[0]
    stop=[False]
    
    def make_request():
        channel=grpc.insecure_channel("localhost:50051")
        stub=PhotosServiceStub(channel)
        while not stop[0]:
            start=time.time()
            try:
                stub.GetPhoto(PhotoRequest(id="1"),timeout=30)
                latencies.append((time.time()-start)*1000)
                count[0]+=1
            except:pass
        channel.close()
    
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures=[executor.submit(make_request) for _ in range(concurrency)]
        time.sleep(DURATION)
        stop[0]=True
        for f in futures:f.result()
    
    latencies.sort()
    rps=count[0]/DURATION
    avg=sum(latencies) / len(latencies) if latencies else 0
    p50=latencies[len(latencies)//2] if latencies else 0
    p95=latencies[int(len(latencies)*0.95)] if latencies else 0
    p99=latencies[int(len(latencies)*0.99)] if latencies else 0
    
    print(f"gRPC  |{concurrency:>5} |{rps:>8.0f}| {avg:>7.1f} |{p50:>7.1f} |{p95:>7.1f} |{p99:>7.1f} |{count[0]:>6}")

print("Сервис|Подкл.|   RPS  |Сред.(мс)| P50(мс)| P95(мс)| P99(мс)| Запросов")
print("------|------|--------|---------|--------|--------|--------|--------")

for c in CONNECTIONS:
    test_rest(c)
    test_grpc(c)
