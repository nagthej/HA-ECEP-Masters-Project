#!/bin/bash
#script for container migration

#Get container id
id=$(docker ps -aqf "name=looper2")

echo "Checkpointing running container..."
echo "Dumping process tree to file system directory..."
docker checkpoint create --checkpoint-dir=/home/$USER/Desktop/"checkpoints" looper2 $id

echo "Trasferring dump files to new container..."
docker create --name looper-clone --security-opt seccomp:unconfined busybox \
         /bin/sh -c 'i=0; while true; do echo $i; i=$(expr $i + 1); sleep 1; done'

echo "Restoring process tree..."
echo "Starting container from checkpoint..."
docker start --checkpoint-dir=/home/$USER/Desktop/checkpoints --checkpoint=$id looper-clone

echo "Restore done"







