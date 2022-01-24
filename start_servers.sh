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
python3 PageServer.py $maxStorageServers & disown
pageServerPid=$!
echo "O servidor de paginas foi iniciado no pid $pageServerPid"

sleep 1

echo "Os servidores de armazenamento serao criados..."
storagePids=()
end=$(($initialPort + $maxStorageServers - 1))
for i in $(seq $initialPort $end); do
    python3 StorageServer.py "server-$i" localhost $i & disown
    serverPid=$!
    storagePids+=($serverPid)
    echo "Servidor $serverPid criado..."
    echo $storagePids
    sleep 1
done

BURN_IT

echo "Matando processo do servidor de paginas de pid $pageServerPid..."
kill -9 $pageServerPid

echo "Matando servidores de armazenamento..."
for i in $storagePids; do
    echo "Matando processo de pid $i..."
    kill -9 $i
done
