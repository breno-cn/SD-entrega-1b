import grpc

PAGE_SERVER_ADDRESS = 'localhost:50051'

with grpc.insecure_channel(PAGE_SERVER_ADDRESS) as channel:
    pass
