from ClientToPage_pb2_grpc import PageStub
from ClientToPage_pb2 import AnnounceRequest

from Hashtable import Hashtable
import sys
import grpc

class StorageServer:

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


server = StorageServer('test', 'localhost', 12345)
