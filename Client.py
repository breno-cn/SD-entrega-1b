from ClientToPage_pb2 import FindRequest
from ClientToPage_pb2_grpc import PageStub

import grpc

PAGE_SERVER_ADDRESS = 'localhost:50051'

with grpc.insecure_channel(PAGE_SERVER_ADDRESS) as channel:
    pageStub = PageStub(channel)

    while True:
        print('O que você deseja fazer?')
        option = int(input('1 -> CREATE\n2 -> READ\n3 -> UPDATE\n4 -> DELETE\n5 -> ENCERRAR\n'))

        # if option == 1:
        #     key = input('Digite a chave: ')
        #     value = input('Digite o valor: ')

        #     status = pageStub.create(CreateRequest(key=key, value=value))
        #     print(str(status))


        # if option == 2:
        #     key = input('Digite a chave: ')
            
        #     resp = pageStub.read(ReadRequest(key=key))
        #     print(str(resp))


        # if option == 3:
        #     key = input('Digite a chave: ')
        #     value = input('Digite o valor: ')

        #     resp = pageStub.update(UpdateRequest(key=key, value=value))
        #     print(str(resp))


        # if option == 4:
        #     key = input('Digite a chave: ')

        #     resp = pageStub.delete(DeleteRequest(key=key))
        #     print(str(resp))


        if option == 5:
            break

        key = input('Digite a chave: ')
        address = pageStub.findKey(FindRequest(key=key))
        print(address)
