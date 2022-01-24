from PageServer_pb2_grpc import PageServicer
from PageServer_pb2_grpc import add_PageServicer_to_server

from PageServer_pb2 import Response
from PageServer_pb2 import FindResponse

from Hashtable import Hashtable
from concurrent import futures
import grpc
import argparse
import sys

def getMaxServers():
    parser = argparse.ArgumentParser()
    parser.add_argument('maxServers', type=int)

    args = parser.parse_args()

    return int(args.maxServers)

class PageServer(PageServicer):
    
    MAX_STORAGE_SERVERS = getMaxServers()

    def __init__(self) -> None:
        super().__init__()
        self.servers = Hashtable()
        self.addressesIndex = [''] * PageServer.MAX_STORAGE_SERVERS
        self.currentStorageServers = 0

    def announce(self, request, context):
        name = request.name
        address = request.address
    
        status = self.servers.create(name, address)
        if status == 4:
            self.addressesIndex[self.currentStorageServers] = address
            self.currentStorageServers += 1

        return Response(status=status)

    def findKey(self, request, context):
        keyBytes = bytes(request.key, 'ascii')
        p = 31
        i = 0
        sum = 0

        for byte in keyBytes:
            sum += byte * (p ** i)

        index = sum % PageServer.MAX_STORAGE_SERVERS

        return FindResponse(address=self.addressesIndex[index])


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_PageServicer_to_server(PageServer(), server)

    server.add_insecure_port('[::]:50051')
    server.start()

    server.wait_for_termination()

serve()
