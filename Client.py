from PageServer_pb2 import FindRequest
from PageServer_pb2_grpc import PageStub

import grpc
from Storage_pb2 import Request

from Storage_pb2_grpc import StorageStub

PAGE_SERVER_ADDRESS = 'localhost:50051'

with grpc.insecure_channel(PAGE_SERVER_ADDRESS) as channel:
    pageStub = PageStub(channel)

    while True:
        print('O que você deseja fazer?')
        option = int(input('1 -> CREATE\n2 -> READ\n3 -> UPDATE\n4 -> DELETE\n5 -> ENCERRAR\n'))

        if option == 5:
            break

        key = input('Digite a chave: ')
        address = pageStub.findKey(FindRequest(key=key)).address
        print(address)

        with grpc.insecure_channel(address) as storageChannel:
            storageStub = StorageStub(storageChannel)

            if option == 1:
                value = input('Digite o valor: ')
                response = storageStub.create(Request(key=key, value=value))
                print(str(response))

            if option == 2:
                response = storageStub.read(Request(key=key))
                print(str(response))

            if option == 3:
                value = input('Digite o valor: ')
                response = storageStub.update(Request(key=key, value=value))
                print(str(response))
            
            if option == 4:
                response = storageStub.delete(Request(key=key))
                print(str(response))
