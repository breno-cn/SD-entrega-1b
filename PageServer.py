from ClientToPage_pb2_grpc import PageServicer
from ClientToPage_pb2_grpc import add_PageServicer_to_server

from ClientToPage_pb2 import Response

from Hashtable import Hashtable
from concurrent import futures
import grpc

class PageServer(PageServicer):
    
    def __init__(self) -> None:
        super().__init__()
        self.servers = Hashtable()

    def announce(self, request, context):
        name = request.name
        address = request.address
    
        status = self.servers.create(name, address)

        return Response(status=status)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_PageServicer_to_server(PageServer(), server)

    server.add_insecure_port('[::]:50051')
    server.start()

    server.wait_for_termination()

serve()
