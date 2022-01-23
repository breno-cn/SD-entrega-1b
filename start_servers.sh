#!/bin/bash

BURN_IT() {
    echo "Pressione qualquer tecla para matar os processos"
    while [ true ] ; do
        read -t 3 -n 1
        if [ $? = 0 ] ; then
            return ;
        else
            echo "..."
        fi
    done
}

maxStorageServers=$1
initialPort=$2

echo "Serao criados $maxStorageServers servidores a partir da porta $initialPort"

echo "Iniciando servidor de paginas..."
python3 PageServer.py $maxStorageServers & 2> /dev/null
pageServerPid=$!
echo "O servidor de paginas foi iniciado no pid $pageServerPid"

sleep 5

echo "Os servidores de armazenamento serao criados..."
storagePids=()
end=$(($initialPort + $maxStorageServers - 1))
for i in $(seq $initialPort $end); do
    python3 StorageServer.py "server-$i" localhost $i & 2> /dev/null
    serverPid=$!
    storagePids+=($serverPid)
    echo "Servidor $serverPid criado..."
    sleep 1
done

echo $storagePids

BURN_IT

echo "Matando processo do servidor de paginas..."
kill -9 $pageServerPid

echo "Matando servidores de armazenamento..."
for i in $storagePids; do
    kill -9 $i
done
