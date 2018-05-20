#!/bin/bash

docker stop looper-clone && docker rm looper-clone
docker stop looper2 && docker rm looper2

docker run -d --name looper2 --security-opt seccomp:unconfined busybox \
         /bin/sh -c 'i=0; while true; do echo $i; i=$(expr $i + 1); sleep 1; done'

