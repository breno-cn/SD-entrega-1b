# SD-entrega-1b

## Subindo os servidores

Para subir os servidores, basta executar:

`sudo ./start_servers.sh $maxServers $initialPort`

Onde `$maxServers` representa o número de servidores de armazenamentos que irão subir, e `$initialPort` representa uma porta inicial a ser contada. Note que os servidores serão criados para ouvir as portas, por exemplo: 100, 101, 102...

## Cliente

Para o cliente, basta executar `python3 Client.py`, que ele irá se conectar ao servidor de páginas na porta `50051`.

Após eles subirem, o script irá matar todos eles quando o usuário pressionar qualquer tecla.

## Possíveis problemas
Caso, por qualquer motivo, o script não mate corretamente os servidores, seus pids estarão escritos no terminal. Um comando `pkill -9 python` ou `pkill -9 python3` consegue também.
