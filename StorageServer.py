from ClientToPage_pb2_grpc import PageStub
from ClientToPage_pb2 import AnnounceRequest

from Storage_pb2_grpc import StorageServicer
from Storage_pb2 import StorageResponse

from Hashtable import Hashtable
from concurrent import futures
import sys
import grpc

class StorageServer(StorageServicer):

    def __init__(self, name: str, host: str, port: int) -> None:
        self.hashtable = Hashtable()
        self.name = name
        self.address = f'{host}:{port}'

        with grpc.insecure_channel('localhost:50051') as channel:
            pageServerStub = PageStub(channel)
            request = AnnounceRequest(name=name, address=self.address)

            print(f'Annoucing server {self.name}...')
            print(str(request))

            status = pageServerStub.announce(request).status
            if status == 5:
                print('Houve algum erro ao criar o servidor de armazenamento!')
                sys.exit(1)
            
            print('Servidor de armazenamento criado com sucesso...')

    def create(self, request, context):
        key = request.key
        value = request.value
        print(f'key {key} value {value}')

        status = self.hashtable.create(key, value)

        return StorageResponse(status=status)
    
    def read(self, request, context):
        key = request.key
        readResponse = self.hashtable.read(key)
        
        print(readResponse)

        if type(readResponse) == str:
            return StorageResponse(status=4, value=readResponse)

        return StorageResponse(status=5, value='')

    def update(self, request, context):
        key = request.key
        value = request.value
        status = self.hashtable.update(key, value)

        return StorageResponse(status=status)

    def delete(self, request, context):
        key = request.key
        status = self.hashtable.delete(key)

        return StorageResponse(status=status)



def serve():
    name = 'test'
    host = 'localhost'
    port = 12345
    storageServer = StorageServer(name, host, port)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # add_PageServicer_to_server(PageServer(), server)

    server.add_insecure_port(f'[::]:{port}')
    server.start()

    server.wait_for_termination()

serve()
